from agent import handle_user_input

def run_chat():
    print("\n🚀 AutoStream AI Agent (Powered by Gemini)")
    print("Type 'exit' or 'quit' to stop the chat.\n")

    while True:
        try:
            user_input = input("You: ").strip()

            # Exit condition
            if user_input.lower() in ["exit", "quit","exit()"]:
                print("\nBot: Thanks for visiting AutoStream! Have a great day 🚀")
                break

            # Empty input handling
            if not user_input:
                print("Bot: Please enter a message.")
                continue

            # Get response from agent
            response = handle_user_input(user_input)

            print(f"Bot: {response}\n")

        except KeyboardInterrupt:
            print("\n\nBot: Chat interrupted. Goodbye! 👋")
            break

        except Exception as e:
            print(f"\nBot: Something went wrong: {str(e)}\n")


if __name__ == "__main__":
    run_chat()