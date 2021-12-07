"""
Contains logic of building GUI for
the Secret Santa Generator application.
"""
import random

from datetime import datetime
from tkinter import Tk, Label, Button, Entry, messagebox

from PIL import ImageTk, Image

from send_email import SendEmail

NO_OF_ENTITIES = 8


class SecretSantaGUI:
    """
    Creates the GUI using tkinter module.
    """
    txt_name = [None] * NO_OF_ENTITIES
    txt_email = [None] * NO_OF_ENTITIES
    txt_gift = [None] * NO_OF_ENTITIES
    txt_date = None
    txt_budget = None

    def __init__(self, root_obj):
        """
        Initializes the Tk() root object for the class.
        """
        self.root_obj = root_obj

    def construct(self):
        """
        Constructs the form as required.
        """
        self.root_obj.title("Welcome to Secret Santa")
        self.root_obj.geometry('600x700')
        
        img = ImageTk.PhotoImage(Image.open('secret_santa.jpeg'))
        panel = Label(self.root_obj, image=img)
        panel.grid(column=0, row=0)
        panel.img = img  # You need to keep a reference to the photo.

        lbl_message = Label(self.root_obj, text="Enter the names, email addresses, and gift ideas for the gift exchange."
                                                "\nThe Secret Santa Generator will handle the rest!",
                            padx=20, pady=10)
        lbl_message.grid(column=0, row=1)

        lbl_name = Label(self.root_obj, text="Name")
        lbl_name.grid(column=0, row=2)
        lbl_email = Label(self.root_obj, text="Email")
        lbl_email.grid(column=1, row=2)
        lbl_email = Label(self.root_obj, text="Gift Idea")
        lbl_email.grid(column=2, row=2)

        for i in range(NO_OF_ENTITIES):
            self.txt_name[i] = Entry(self.root_obj, width=30)
            self.txt_name[i].grid(column=0, row=3 + i, padx=5, pady=5)
            self.txt_email[i] = Entry(self.root_obj, width=30)
            self.txt_email[i].grid(column=1, row=3 + i, padx=5, pady=5)
            self.txt_gift[i] = Entry(self.root_obj, width=30)
            self.txt_gift[i].grid(column=2, row=3 + i, padx=5, pady=5)

        lbl_date = Label(self.root_obj, text="Date of gift exchange: (mm/dd/yyyy)")
        lbl_date.grid(column=0, row=3 + NO_OF_ENTITIES, padx=20, pady=20)
        self.txt_date = Entry(self.root_obj, width=20)
        self.txt_date.grid(column=1, row=3 + NO_OF_ENTITIES, padx=20, pady=20)

        lbl_budget = Label(self.root_obj, text="Budget: (US$)")
        lbl_budget.grid(column=0, row=4 + NO_OF_ENTITIES, padx=5, pady=5)
        self.txt_budget = Entry(self.root_obj, width=20)
        self.txt_budget.grid(column=1, row=4 + NO_OF_ENTITIES, padx=5, pady=5)

        btn = Button(self.root_obj, width=15, text="Send Invitations", \
                     font=("Arial Bold", 10), command=self.send_invitations)
        btn.grid(column=0, row=5 + NO_OF_ENTITIES, padx=10, pady=30)

    def send_invitations(self):
        """
        Assigns secret santa to every participant and sends an email
        invite to respective members informing the same.
        """
        event_date_str = self.txt_date.get()
        if event_date_str:
            try:
                event_date = datetime.strptime(event_date_str, '%m/%d/%Y')
            except ValueError:
                messagebox.showerror("Error", "Invalid date format.")
                return

            event_date_str = datetime.strftime(event_date, "%A - %d %b, %Y")
        else:
            event_date_str = '-'

        budget = self.txt_budget.get()
        try:
            budget = int(budget)
        except ValueError:
            messagebox.showerror("Error", "Invalid budget value.")
            return

        email_dict = {}
        gift_dict = {}
        participants = []
        for i in range(NO_OF_ENTITIES):
            email = self.txt_email[i].get()
            name = self.txt_name[i].get()
            gift = self.txt_name[i].get()
            if name and email and gift:
                email_dict[email] = name
                participants.append(email)
                gift_dict[email] = gift
            else:
                if email and gift and not name:
                    messagebox.showerror("Error", f"Name not found for entity no. {i+1}.")
                    return

                if name and gift and not email:
                    messagebox.showerror("Error", f"Email mandatory for entity no. {i+1}.")
                    return
                
                if email and name and not gift:
                    messagebox.showerror("Error", f"Gift mandatory for entity no. {i+1}.")
                    return

        if (len(participants)) < 2:
            messagebox.showerror("Error", "Insufficient participants.")
            return

        random.shuffle(participants)

        email_formatter = EmailFormatter(event_date_str, budget)
        for i, _ in enumerate(participants):
            giver = participants[i]
            receiver = participants[(i + 1) % (len(participants))]
            send_email = SendEmail(['smtp.gmail.com', 587, \
                                    'abcdef@gmail.com', 'xxxxxxxxx'], True)
            send_email.send(from_name="Secret Santa Generator",
                            to_address=[giver], \
                            subject=email_formatter.subject(email_dict[giver]), \
                            body=email_formatter.body(email_dict[giver], \
                                                      email_dict[receiver], gift_dict[receiver]))

        messagebox.showinfo("Success", "Invitations sent.")


class EmailFormatter:
    """
    Specifies the email subject and body content for invitations.
    """

    def __init__(self, _date, budget):
        """
        Initialize date and budget of the invitation.
        """
        self._date = _date
        self.budget = budget

    @staticmethod
    def subject(name1):
        """
        Subject matter of the email.
        """
        return f'{name1}, you have drawn a name for Secret Santa!'

    def body(self, name1, name2, gift):
        """
        Body content of the email.
        """
        return f"Hi {name1},\nThe names have been drawn using the Python Secret Santa Generator. " \
               f"Find below your drawn name.\n" \
               f"\n{name2}\n" \
               f"A gift idea for {name2} is {gift}.\n" \
               f"Date of gift exchange: {self._date}\n" \
               f"Budget: US$ {self.budget}\n" \
               f"\nHave Fun!\n" \
               f"- Powered by Python"


def main():
    """
    Entry-point of the function.
    """
    root = Tk()
    SecretSantaGUI(root).construct()
    root.mainloop()


if __name__ == "__main__":
    main()
