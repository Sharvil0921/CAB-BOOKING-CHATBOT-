
# import random

# # ---------- Predefined data ----------
# # Cab type -> rate per km (Rs)
# CAB_NAMES = {1: "Auto", 2: "Sedan", 3: "SUV"}
# CAB_RATES = {1: 12, 2: 18, 3: 25}

# # Route number -> (source, destination, distance in km)
# ROUTES = {
#     1: ("Pune Station", "Shivajinagar", 5),
#     2: ("Swargate", "Kothrud", 8),
#     3: ("Hinjawadi", "Wakad", 10),
# }


# def read_choice(prompt):
#     """Read an integer from the user. Returns None if the input is not a number."""
#     try:
#         text = input(prompt).strip()
#     except (EOFError, KeyboardInterrupt):
#         print("\nInput interrupted. Exiting the program.")
#         raise SystemExit

#     if text.isdigit():
#         return int(text)
#     return None


# def book_ride():
#     # Step 2: choose cab type
#     print("\n--- Choose Cab Type ---")
#     print("1. Auto  (Rs.12/km)")
#     print("2. Sedan (Rs.18/km)")
#     print("3. SUV   (Rs.25/km)")
#     cab = read_choice("Enter your choice (1-3): ")
#     if cab not in CAB_NAMES:
#         print("Invalid cab choice! Returning to main menu.")
#         return

#     # Step 3: choose route
#     print("\n--- Choose Route ---")
#     for number, (source, destination, km) in ROUTES.items():
#         print(f"{number}. {source} to {destination} ({km} km)")
#     route = read_choice("Enter your choice (1-3): ")
#     if route not in ROUTES:
#         print("Invalid route choice! Returning to main menu.")
#         return

#     # Step 4: calculate fare
#     source, destination, distance = ROUTES[route]
#     rate = CAB_RATES[cab]
#     fare = rate * distance

#     print("\n===== Ride Summary =====")
#     print(f"Cab Type    : {CAB_NAMES[cab]}")
#     print(f"Source      : {source}")
#     print(f"Destination : {destination}")
#     print(f"Distance    : {distance} km")
#     print(f"Rate        : Rs.{rate}/km")
#     print(f"Total Fare  : Rs.{fare}  ({distance} x {rate})")
#     print("========================")

#     # Step 5: cancellation allowed ONLY before the OTP is shared
#     while True:
#         print("\n1. Confirm & Share OTP")
#         print("2. Cancel Ride")
#         confirm = read_choice("Enter your choice (1-2): ")

#         if confirm == 2:
#             print("\nYour ride has been cancelled. No OTP was shared.")
#             return
#         elif confirm == 1:
#             break
#         else:
#             print("Invalid choice! Please enter 1 or 2.")

#     # Step 6: generate OTP and lock the ride
#     otp = random.randint(1000, 9999)  # 4-digit OTP
#     print(f"\nOTP shared with you: {otp}")
#     print("NOTE: Once the OTP is shared, the ride CANNOT be cancelled.")
#     print("Booking confirmed! Your driver is on the way. Share the OTP with the driver at pickup.")


# def main():
#     print("Welcome to the Cab Booking Chatbot!")

#     # Step 1: main menu runs until the user chooses Exit
#     while True:
#         print("\n===== MAIN MENU =====")
#         print("1. Book Ride")
#         print("2. Exit")
#         choice = read_choice("Enter your choice (1-2): ")

#         if choice == 1:
#             book_ride()
#         elif choice == 2:
#             # Step 7: exit
#             print("\nThank you for using the Cab Booking Chatbot. Goodbye!")
#             break
#         else:
#             print("Invalid choice! Please enter 1 or 2.")


# if __name__ == "__main__":
#     main()
