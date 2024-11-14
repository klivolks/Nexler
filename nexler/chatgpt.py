from nexler.services.ChatGPT import ChatGPT


def ai(args):
    gpt = ChatGPT()
    func = args.function
    if func == 'code':
        gpt.file = args.file
        gpt.instruction = args.instruction
        gpt.code(start_line=args.start, end_line=args.end)
    elif func == 'create':
        gpt.instruction = args.instruction
        result = gpt.create()
        print(result)
    elif func == 'insert':
        gpt.file = args.file
        gpt.instruction = args.instruction
        gpt.insert()
    elif func == 'edit':
        gpt.file = args.file
        gpt.instruction = args.instruction
        gpt.edit()


