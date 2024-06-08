import shelve

def save_highest_score(score):
    old_score = load_highest_score()
    if(score > old_score):
     with shelve.open('game_data') as shelf:
         shelf['highest_score'] = score
    else:
       pass
    
def load_highest_score():
    with shelve.open('game_data') as shelf:
        return shelf.get('highest_score', 0)