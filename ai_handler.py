import google.generativeai as genai
from config import GEMINI_API_KEY

class AIChatHandler:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.chat = self.model.start_chat(history=[])
        
    async def get_response(self, message: str) -> str:
        try:
            # Add expense tracking context to every prompt
            context = """You are a helpful and friendly expense tracking assistant. 
            You can help users track their expenses and provide financial advice. 
            Available commands: 
            /add [amount] [category] [note] - Add an expense
            /summary - View monthly summary
            /categories - View expenses by category
            
            If user asks about adding expense, guide them to use the /add command.
            """
            
            prompt = f"{context}\n\nUser message: {message}"
            response = self.chat.send_message(prompt)
            return response.text
            
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"