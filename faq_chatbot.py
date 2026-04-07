import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
except ImportError:
    print("Installing sklearn... please wait")
    install('scikit-learn')
    from sklearn.feature_extraction.text import TfidfVectorizer
import customtkinter as ctk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. قاعدة البيانات (الأسئلة والأجوبة)
faq_data = {
    
    "What is Artificial Intelligence?": "AI is a branch of computer science that builds smart machines capable of performing human-like tasks.",
    "How can I join the internship?": "You can join by applying through the CodeAlpha website or following instructions in the WhatsApp group.",
    "What tasks are required for the certificate?": "You must complete at least 2 or 3 tasks from the assigned project list.",
    "Which programming language is used?": "We primarily use Python for AI and Machine Learning tasks.",
    "How do I submit my work?": "Submit your work by providing your GitHub repository link and LinkedIn post in the official submission form.",
    "What is the duration of this internship?": "The internship typically lasts for 4 weeks (one month)."
    #"Hi?": "How are you.  How can I help you."
}

questions = list(faq_data.keys())

class ChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CodeAlpha FAQ Chatbot")
        self.geometry("500x600")

        # واجهة الشات
        self.chat_display = ctk.CTkTextbox(self, width=460, height=400, state="disabled")
        self.chat_display.pack(pady=20)

        self.input_entry = ctk.CTkEntry(self, width=350, placeholder_text="Type your question here...")
        self.input_entry.pack(side="left", padx=20, pady=10)

        self.send_btn = ctk.CTkButton(self, text="send", width=80, command=self.get_response)
        self.send_btn.pack(side="right", padx=10, pady=10)

    def get_response(self):
        user_query = self.input_entry.get()
        if not user_query: return

        # خوارزمية البحث عن أقرب سؤال (NLP Logic)
        vectorizer = TfidfVectorizer().fit_transform(questions + [user_query])
        vectors = vectorizer.toarray()
        
        # حساب التشابه بين سؤال المستخدم وكل الأسئلة اللي عندنا
        cosine_sim = cosine_similarity([vectors[-1]], vectors[:-1])
        best_match_idx = cosine_sim.argmax()
        
        # لو التشابه أكبر من نسبة معينة (مثلاً 0.2) يجاوب، غير كدة يقول مش عارف
        if cosine_sim[0][best_match_idx] > 0.2:
            reply = faq_data[questions[best_match_idx]]
        else:
            reply = "I'm sorry, I don't have information about that"

        self.update_chat("أنت", user_query)
        self.update_chat("البوت", reply)
        self.input_entry.delete(0, 'end')

    def update_chat(self, sender, message):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"{sender}: {message}\n\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

if __name__ == "__main__":
    app = ChatbotApp()
    app.mainloop()
    #python -c "import sklearn; print('Success!')"