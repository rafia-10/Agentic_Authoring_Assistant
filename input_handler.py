def collect_user_input():
    user_input = {}

    user_input['description'] = input("Enter your project description: ")
    user_input['repo'] = input("Enter repository link (optional): ")
    user_input['dataset'] = input("Enter dataset info (optional): ")
    user_input['results'] = input("Enter experiment results (optional): ")

    print("User input collected:", user_input)
