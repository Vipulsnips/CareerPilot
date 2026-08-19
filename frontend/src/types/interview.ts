export interface InterviewQuestion {
  question: string;
  category: string;
  difficulty: string;
}

export interface InterviewQuestions {
  questions: InterviewQuestion[];
}