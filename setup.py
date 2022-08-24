import pickle

with open('next_marking_img_id.pkl', 'wb') as file:
    # A new file will be created
    pickle.dump(1, file)

with open('already_recommended_img_ids.pkl', 'wb') as file:
    # A new file will be created
    pickle.dump([], file)

with open('is_model_up_to_date.pkl', 'wb') as file:
    # A new file will be created
    pickle.dump(False, file)

with open('last_moved_img_id.pkl', 'wb') as file:
    # A new file will be created
    pickle.dump(0, file)

with open('last_sneakers_amount.pkl', 'wb') as file:
    # A new file will be created
    pickle.dump(0, file)
