export interface Education {
  institution: string | null;
  degree: string | null;
  field: string | null;
  cgpa: number | null;
  start_year: number | null;
  end_year: number | null;
}

export interface Experience {
  company: string | null;
  role: string | null;
  duration: string | null;
  description: string | null;
}

export interface Project {
  title: string | null;
  description: string | null;
  technologies: string[];
}

export interface Resume {
  name: string | null;
  email: string | null;
  phone: string | null;
  github: string | null;
  linkedin: string | null;
  summary: string | null;

  skills: string[];
  education: Education[];
  experience: Experience[];
  projects: Project[];
}

export interface ResumeAnalysis {
  strengths: string[];
  weaknesses: string[];
  skill_gaps: string[];
  recommended_topics: string[];
}