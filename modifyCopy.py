import configparser
import os
import time


def read_ini_file(file_path):
    config = configparser.ConfigParser(delimiters='⇒')
    config.optionxform = str
    config.read(file_path)

    return config


def get_replacement_rules(config):
    rules = {}
    for section in config.sections():
        for key, value in config.items(section):
            search_string = f"{key}"
            replace_string = f"{value}"
            rules[search_string] = replace_string
    return rules


def replace_values_in_files(config, source_folder, output_folder):
    replacement_rules = get_replacement_rules(config)
    for root, _, files in os.walk(source_folder):
        for filename in files:
            source_file_path = os.path.join(root, filename)

            if os.path.isfile(source_file_path) and source_file_path.endswith('.xml'):
                with open(source_file_path, 'r', encoding='utf-8') as source_file:
                    content = source_file.read()
                    lines = source_file.readlines()
                # for section in config.sections():
                #     for key, value in config.items(section):
                #         search_string = f"{key}"
                #         replace_string = f"{value}"
                #
                #         if search_string in content:
                #             content = content.replace(search_string, replace_string)
                #             relative_path = os.path.relpath(source_file_path, source_folder)
                #             output_file_path = os.path.join(output_folder, "modified", relative_path)
                #             os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                #             print(f"write file: {output_file_path}")
                #             with open(output_file_path, 'w', encoding='utf-8') as output_file:
                #                 output_file.write(content)
                for search_string, replace_string in replacement_rules.items():
                    content = content.replace(search_string, replace_string)

                relative_path = os.path.relpath(source_file_path, source_folder)
                output_file_path = os.path.join(output_folder, "modified", relative_path)
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    print(f"write file: {output_file_path}")
                    output_file.write(content)


if __name__ == "__main__":
    start_time = time.time()
    ini_file_path = "E:\\replace\\config.ini"
    source_folder_path = "E:\\replace\\1"
    output_folder_path = "E:\\replace\\2"

    # if not os.path.exists(output_folder_path):
    #    os.mkdir(output_folder_path)

    config_data = read_ini_file(ini_file_path)
    replace_values_in_files(config_data, source_folder_path, output_folder_path)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"total time costed:{total_time:.2f}s")
