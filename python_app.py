import customtkinter as ctk
import threading
from tkinter import filedialog
import engine

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def load_document_thread(file_path, should_save, status_label, load_button, save_checkbox, chat_history):
    try:
        engine.load_document(file_path, should_save)
        msg = "Document loaded and indexed successfully."
    except Exception as e:
        msg = str(e)
        
    status_label.configure(text=msg)
    chat_history.configure(state="normal")
    chat_history.insert("end", f"System: {msg}\n\n")
    chat_history.configure(state="disabled")
    load_button.configure(state="normal")
    save_checkbox.configure(state="normal")

def select_file(status_label, load_button, save_checkbox, chat_history):
    file_path = filedialog.askopenfilename(filetypes=[("Documents", "*.pdf *.docx *.txt")])
    if file_path:
        status_label.configure(text="Loading and indexing...")
        load_button.configure(state="disabled")
        save_checkbox.configure(state="disabled")
        should_save = save_checkbox.get() == 1
        
        threading.Thread(
            target=load_document_thread, 
            args=(file_path, should_save, status_label, load_button, save_checkbox, chat_history),
            daemon=True
        ).start()

def process_query(query, chat_history, send_button):
    answer = engine.get_answer(query)
    chat_history.configure(state="normal")
    chat_history.insert("end", f"AI: {answer}\n\n")
    chat_history.configure(state="disabled")
    chat_history.see("end")
    send_button.configure(state="normal")

def handle_send(input_field, chat_history, send_button):
    user_text = input_field.get().strip()
    if not user_text:
        return

    chat_history.configure(state="normal")
    chat_history.insert("end", f"You: {user_text}\n\n")
    chat_history.configure(state="disabled")
    chat_history.see("end")
    
    input_field.delete(0, 'end')
    send_button.configure(state="disabled")

    threading.Thread(
        target=process_query, 
        args=(user_text, chat_history, send_button), 
        daemon=True
    ).start()

def main():
    app = ctk.CTk()
    app.title("ChatAI")
    app.geometry("900x700")
    
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=1)

    top_frame = ctk.CTkFrame(app, fg_color="transparent")
    top_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="ew")
    
    save_checkbox = ctk.CTkCheckBox(top_frame, text="Save to docs/")
    save_checkbox.pack(side="left", padx=(0, 10))

    load_button = ctk.CTkButton(top_frame, text="Load Document", 
                                command=lambda: select_file(status_label, load_button, save_checkbox, chat_history))
    load_button.pack(side="left")

    status_label = ctk.CTkLabel(top_frame, text="Ready", text_color="gray")
    status_label.pack(side="left", padx=(10, 0))

    chat_history = ctk.CTkTextbox(app, state="disabled", font=("Segoe UI", 14), wrap="word")
    chat_history.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

    input_field = ctk.CTkEntry(app, placeholder_text="Ask a question...", font=("Segoe UI", 14))
    input_field.grid(row=2, column=0, padx=(20, 10), pady=(0, 20), sticky="ew")

    send_button = ctk.CTkButton(app, text="Send", font=("Segoe UI", 14), 
                                command=lambda: handle_send(input_field, chat_history, send_button))
    send_button.grid(row=2, column=1, padx=(0, 20), pady=(0, 20))

    app.bind('<Return>', lambda event: handle_send(input_field, chat_history, send_button))
    
    app.mainloop()

if __name__ == "__main__":
    main()