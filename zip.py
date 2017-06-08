#**********************************************************************
# Description:
#    Zips the contents of a folder.
# Parameters:
#   0 - Input folder.
#   1 - Output zip file. It is assumed that the user added the .zip 
#       extension.  
#**********************************************************************

# Import modules and create the geoprocessor
#
import sys, zipfile, os
import tempfile


# Function for zipping files.  If keep is true, the folder, along with 
#  all its contents, will be written to the zip file.  If false, only 
#  the contents of the input folder will be written to the zip file - 
#  the input folder name will not appear in the zip file.
#
def zipws(path, excludes = [], keep=False):
    outfile = tempfile.NamedTemporaryFile(delete=True)
    zip = zipfile.ZipFile(outfile, 'w', zipfile.ZIP_DEFLATED)

    path = os.path.normpath(path)
    # os.walk visits every subdirectory, returning a 3-tuple
    #  of directory name, subdirectories in it, and file names
    #  in it.
    #
    for (dirpath, dirnames, filenames) in os.walk(path):
        exclude = False
        for e in excludes:
            if dirpath[len(path)+1:].startswith(e):
                exclude = True
                print("Exclude " + dirpath)
                break
        if exclude:
            continue
        # Iterate over every file name
        #
        for file in filenames:
            # Ignore .lock files
            #
            if file.endswith('.lock'):
                continue

            try:
                if keep:
                    zip.write(os.path.join(dirpath, file),
                    os.path.join(os.path.basename(path), os.path.join(dirpath, file)[len(path)+len(os.sep):]))
                else:
                    zip.write(os.path.join(dirpath, file),
                    os.path.join(dirpath[len(path):], file))

            except Exception, e:
                print("WARNING: Error adding %s: %s"  % (file,e))

    # get the file as binary
    zip.close()
    outfile = open(outfile.name,"rb")
    binary = outfile.read()
    outfile.close()
    return binary

