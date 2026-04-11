import Link from "next/link";

const courses = [
  { title: "Claude Agent System Engineering", slug: "claude-agent-system", modules: 10, level: "Advanced" },
  { title: "AWS Cloud Practitioner to Solutions Architect", slug: "aws-cloud", modules: 12, level: "Beginner-Advanced" },
  { title: "Azure Cloud Engineering", slug: "azure-cloud", modules: 10, level: "Beginner-Advanced" },
  { title: "GCP Cloud Engineering", slug: "gcp-cloud", modules: 10, level: "Beginner-Advanced" },
  { title: "Cloud AI & Machine Learning", slug: "cloud-ai-ml", modules: 12, level: "Intermediate" },
  { title: "DevOps & SDLC Mastery", slug: "devops-sdlc", modules: 10, level: "Intermediate" },
  { title: "DevOps with Terraform", slug: "devops-terraform", modules: 8, level: "Intermediate" },
  { title: "Cloud Security", slug: "cloud-security", modules: 12, level: "Intermediate-Advanced" },
  { title: "Product Management", slug: "product-management", modules: 10, level: "All Levels" },
  { title: "Project Management", slug: "project-management", modules: 10, level: "All Levels" },
  { title: "ServiceNow Administration", slug: "servicenow", modules: 8, level: "Beginner" },
  { title: "SAP Enterprise Systems", slug: "sap", modules: 10, level: "Beginner-Intermediate" },
  { title: "Oracle Cloud Infrastructure", slug: "oracle-cloud", modules: 10, level: "Intermediate" },
  { title: "Cloud Programming", slug: "cloud-programming", modules: 12, level: "Beginner-Advanced" },
  { title: "Cloud Career Acceleration", slug: "cloud-career", modules: 8, level: "All Levels" },
  { title: "Enterprise Multi-Cloud", slug: "enterprise-multicloud", modules: 10, level: "Advanced" },
  { title: "Cloud Fundamentals", slug: "cloud-fundamentals", modules: 8, level: "Beginner" },
];

export default function CoursesPage() {
  return (
    <main className="min-h-screen bg-ink">
      <section className="py-20 text-center">
        <span className="inline-block bg-green/10 text-green text-xs font-semibold px-3 py-1 rounded-full border border-green/20 mb-4">
          100% FREE
        </span>
        <h1 className="font-syne text-4xl md:text-5xl font-bold bg-gradient-to-r from-white to-cyan bg-clip-text text-transparent mb-4">
          17 Free Cloud Courses
        </h1>
        <p className="text-gray2 text-lg max-w-2xl mx-auto">
          Enterprise-grade curriculum. No credit card. No paywall. Built from real production experience.
        </p>
      </section>
      <section className="max-w-7xl mx-auto px-4 pb-20 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {courses.map((course) => (
          <Link
            key={course.slug}
            href={`/courses/${course.slug}`}
            className="bg-card border border-edge rounded-lg p-6 hover:border-cyan/40 hover:-translate-y-1 transition-all group"
          >
            <span className="inline-block bg-green/10 text-green text-[10px] font-semibold px-2 py-0.5 rounded-full border border-green/20 uppercase mb-3">
              Free
            </span>
            <h3 className="text-white text-lg font-semibold mb-2 group-hover:text-cyan transition-colors">
              {course.title}
            </h3>
            <div className="flex items-center gap-4 text-gray text-xs mt-4">
              <span>{course.modules} modules</span>
              <span className="w-1 h-1 bg-edge2 rounded-full" />
              <span>{course.level}</span>
            </div>
          </Link>
        ))}
      </section>
    </main>
  );
}
