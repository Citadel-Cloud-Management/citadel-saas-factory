"""Stripe webhook handler."""
import os
import json
from fastapi import APIRouter, Request, HTTPException
from sqlalchemy import select
from app.core.database import async_session
from app.models.order import Order, OrderStatus
from app.models.user import User

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

@router.post("/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    try:
        event = json.loads(payload)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    event_type = event.get("type", "")
    data = event.get("data", {}).get("object", {})
    async with async_session() as db:
        if event_type == "payment_intent.succeeded":
            pi_id = data.get("id")
            result = await db.execute(select(Order).where(Order.stripe_payment_intent_id == pi_id))
            order = result.scalar_one_or_none()
            if order:
                order.status = OrderStatus.paid
                await db.commit()
        elif event_type == "customer.subscription.updated":
            customer_id = data.get("customer")
            status = data.get("status")
            result = await db.execute(select(User).where(User.stripe_customer_id == customer_id))
            user = result.scalar_one_or_none()
            if user:
                user.subscription_status = status
                await db.commit()
    return {"received": True}
