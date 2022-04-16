from os import walk, path


class File_Searcher:
    def __init__(self, file_extension=None, search_folder='Model_File_Folder', output_file='file_list', limit=2000):
        """
        :param file_extension: tuple of strings of file extensions which need to search in the search_folder. by default
          file_extension = ['.STL', '.stl']
        :param search_folder: Folder name where files will be searched
        :param output_file: .txt file name which will have all the file path which have file extension == file_extension
        """
        assert path.isdir(search_folder)
        self.output_file = output_file
        self.limit = limit
        self.search_folder = search_folder
        if file_extension is None:
            file_extension = ['.STL', '.stl']
        self.file_extension = file_extension
        self.generate_file()

    def generate_file(self):
        output_file_count = 1
        text_file = open(f"{self.output_file}_{output_file_count}.txt", 'w')
        count = 0
        for r, d, files in walk(self.search_folder):
            for file in files:
                _, extension = path.splitext(file)
                if extension in self.file_extension:
                    text_file.write(path.join(r, file) + '\n')
                    count += 1
                    if count >= self.limit:
                        text_file.close()
                        output_file_count += 1
                        text_file = open(f"{self.output_file}_{output_file_count}.txt", 'w')
                        count = 0


if __name__ == "__main__":
    # lis = ['test', 'train']
    # for name in lis:
    File_Searcher(search_folder='CADNET_3317', output_file='file_list',
                  limit=2000)
