def transport(todo):
    # Выбираем действие
    rest =0
    if(todo == 'tdcheck'):
        print('tdcheck called')
        rest = 1

    if(todo == 'twcheck'):
        print('twcheck called')
        rest = 1
    return rest


