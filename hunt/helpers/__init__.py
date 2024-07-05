import os


def is_initialized():
    initialized = True
    if os.name == 'nt':
        data_dir = f'{os.getenv("LOCALAPPDATA")}\hunt'
    else:
        data_dir = f'{os.path.join(os.path.expanduser("~"), ".hunt")}'
    
    try:
        db_size = os.path.getsize(os.path.join(data_dir, 'hunt.db'))
        if not db_size or db_size == 0:
            print('Empty database file. Please re-run the "init" command.')
            initialized = False
    except:
        print('Database not initialized. Please run the "init" command first.')
        initialized = False
    
    return initialized