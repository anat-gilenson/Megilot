from megilot import app
import os
import datetime
import shutil


def allowed_file(filename):
    """Check if filename is of an allowed type. 

    Args:
        filename (str): file name to determine if it's allowed.

    Returns:
        boolean: filename is allowed or not.
    """
    # We only want files with a . in the filename
    if not "." in filename:
        return False

    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is in ALLOWED_FILE_EXTENSIONS
    if ext.upper() in app.config['ALLOWED_FILE_EXTENTIONS']:
        return True
    else:
        return False



def clear_old_texts():
    """Delete directories 'older' then 30 minutes in app.config['TEXT_UPLOADS']"""
    for root, dirs, files in os.walk(app.config['TEXT_UPLOADS']):
        for d in dirs:
            dirpath = os.path.join(app.config['TEXT_UPLOADS'], d)
            dir_modified = datetime.datetime.fromtimestamp(os.path.getmtime(dirpath))
            if datetime.datetime.now() - dir_modified > datetime.timedelta(minutes=30):
                try:
                    shutil.rmtree(os.path.join(app.config['TEXT_UPLOADS'], d))
                except Exception as e:
                    print(e)
                    print('Exception while trying to clear directory')

def texts_from_dir(path):
    """Retrive a dictionary of texts representing every text in every txt file in path. 

    Args:
        path (str): path to search texts in.

    Returns:
        dict: dictionary of filename:text pairs composed of all text files in path. 
    """
    res={}
    if os.path.exists(path):
        for filename in os.listdir(path):
            if filename!="results.pickle":
                filepath=os.path.join(path,filename)
                try:
                    f=open(filepath, "r")
                    text=f.read()
                except OSError as e:
                    print(e)
                    print('file dosnt exist anymore.')
                    return None
                else:
                    res[filename]=text
                    f.close()
    return res
