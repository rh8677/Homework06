# Raymond Hu 4/2/22
import csv
import math
import sys


all_splits = []  # A list of all the splits (attribute and threshold) that happens within the ideal decision tree
all_age = []  # A list of all the ages in the given csv data
all_height = []  # A list of all the heights in the given csv data
all_tail = []  # A list of all the tail lengths in the given csv data
all_hair = []  # A list of all the hair lengths in the given csv data
all_bang = []  # A list of all the bang lengths in the given csv data
all_reach = []  # A list of all the reaches in the given csv data


# This function will determine the entropy of a set of records.
#
# argument 1 (set_of_records) - the set of records that we need to analyze
def cal_entropy(set_of_records):
    # If there are no records in the list, we exit
    if len(set_of_records) == 0:
        return 0

    assam = 0
    bhutan = 0
    for a_record in set_of_records:
        # If the eighth attribute of the record (class id) is 1, it is Bhutan
        if a_record[7] == 1:
            bhutan += 1

        # Otherwise it is Assam
        else:
            assam += 1

    p_of_assam = assam / (assam + bhutan)  # P(assam) is the amount of assams over the total classes
    p_of_bhutan = bhutan / (assam + bhutan)  # P(bhutan) is the amount of bhutans over the total classes

    # If p_of_assam is 0, we cannot perform the log operation on it
    if p_of_assam == 0:
        if p_of_bhutan == 0:
            entropy = 0
        else:
            entropy = -(p_of_bhutan * math.log(p_of_bhutan))

    # If p_of_bhutan is 0, we cannot perform the log operation on it
    elif p_of_bhutan == 0:
        if p_of_assam == 0:
            entropy = 0
        else:
            entropy = -(p_of_assam * math.log(p_of_assam))

    # Otherwise we perform the complete formula for entropy:
    # Entropy = negative (P(assam) x log(P(assam)) + P(bhutan) x log(P(bhutan))
    else:
        entropy = -((p_of_bhutan * math.log(p_of_bhutan)) + (p_of_assam * math.log(p_of_assam)))
    return entropy


# This function will determine whether there are more Assams or Bhuttans in a particular set of records.
#
# argument 1 (set_of_records) - the set of records that we need to analyze
def more_class(set_of_records):
    assam = 0
    bhutan = 0
    for a_record in set_of_records:
        # If the eighth attribute of the record (class id) is 1, it is Bhutan
        if a_record[7] == 1:
            bhutan += 1

        # Otherwise it is Assam
        else:
            assam += 1

    # Return the class with the higher count
    if assam > bhutan:
        return -1
    else:
        return 1


# This function will determine the percentage of the majority class (Assam or Bhuttan)
# over the total classes.
#
# argument 1 (set_of_records) - the set of records that we need to analyze
def more_percent(set_of_records):
    assam = 0
    bhutan = 0
    for a_record in set_of_records:
        # If the eighth attribute of the record (class id) is 1, it is Bhutan
        if a_record[7] == 1:
            bhutan += 1

        # Otherwise it is Assam
        else:
            assam += 1

    # Return the percentage of the majority class
    if assam > bhutan:
        return assam / (assam + bhutan)
    else:
        return bhutan / (assam + bhutan)


# This function will determine the best attribute and threshold to split a list of records by determining
# the least weighted entropy. It will keep calling itself recursively until the stopping criteria are met.
#
# argument 1 (the_records) - the set of records that we need to analyze and gather info from
# argument 2 (depth) - the depth of the current node out of the entire decision tree
def best_split(the_records, depth):
    # major_class = more_class(the_records)
    major_percent = more_percent(the_records)
    # if depth > 10 or len(the_records) < 9 or major_percent > 0.95:
    #     return major_class
    # else:
    #     best_attribute = 0
    #     best_threshold = min(all_age)
    #     best_entropy = 1
    best_threshold = min(all_age)
    current_threshold = min(all_age)
    best_entropy = 1
    while current_threshold <= max(all_age):
        node1 = []
        node2 = []
        for a_record in the_records:
            if a_record[0] <= current_threshold:
                node1.append(a_record)
            else:
                node2.append(a_record)

        wei_entropy = ((len(node1) / len(the_records)) * cal_entropy(node1)) + ((len(node2) / len(the_records))
                                                                                * cal_entropy(node2))

        if wei_entropy < best_entropy:
            best_entropy = wei_entropy
            best_threshold = current_threshold

        current_threshold += 1

    all_splits.append(['Age', best_threshold])


# This function will build a trained program (a python file called 'HW05_Classifier_Hu.py') which will
# utilize the decision tree built by best_split in order to determine which class each record of a csv
# file falls into.
def write_trained_program():
    mentee_program = open("HW05_Classifier_Hu.py", "w")
    mentee_program.write("import csv\n")
    mentee_program.write("import sys\n")
    mentee_program.write("\n")
    mentee_program.write("\n")
    mentee_program.write("# This function reads the csv file specified in the command line, and classifies each row of "
                         "data into one of\n")
    mentee_program.write("# two classes.\n")
    mentee_program.write("if __name__ == '__main__':\n")
    mentee_program.write("    # If the amount of arguments (plus the name of the program) is not 2, we will inform the "
                         "user.\n")
    mentee_program.write("    if len(sys.argv) != 2:\n")
    mentee_program.write("        print(\"Error - invalid number of arguments (must specify the csv file)\")\n")
    mentee_program.write("    else:\n")
    mentee_program.write("        try:\n")
    mentee_program.write("            # The second cmd argument is the csv file we have to open and retrieve data "
                         "from\n")
    mentee_program.write("            with open(sys.argv[1]) as csv_file:\n")
    mentee_program.write("                read_data = csv.reader(csv_file)\n")
    mentee_program.write("                output_file = open(\"output.csv\", \"w\", newline=\"\")  # Puts the "
                         "classified data into another csv file\n")
    mentee_program.write("                write_data = csv.writer(output_file)\n")
    mentee_program.write("                header = next(read_data)\n")
    mentee_program.write("                header.append('Class')\n")
    mentee_program.write("                write_data.writerow(header)  # Puts the header in the output file\n")
    mentee_program.write("                for row in read_data:\n")
    mentee_program.write("                    the_float = float(row[0].strip())\n")
    mentee_program.write("                    rounded_num = round(the_float / 2) * 2\n")
    mentee_program.write("\n")
    mentee_program.write("                    # If the normalized age is less than the number specified, it will "
                         "belong in the Assam class\n")
    mentee_program.write("                    if rounded_num <= " + str(all_splits[0][1]) + ":\n")
    mentee_program.write("                        row.append('+1')\n")
    mentee_program.write("                        write_data.writerow(row)\n")
    mentee_program.write("\n")
    mentee_program.write("                    # If the normalized age is greater than the number specified, it "
                         "will belong in the Bhutan\n")
    mentee_program.write("                    # class instead\n")
    mentee_program.write("                    else:\n")
    mentee_program.write("                        row.append('-1')\n")
    mentee_program.write("                        write_data.writerow(row)\n")
    mentee_program.write("            csv_file.close()\n")
    mentee_program.write("            output_file.close()\n")
    mentee_program.write("\n")
    mentee_program.write("        # If the file is unable to be opened for whatever reason, we will inform the user.\n")
    mentee_program.write("        except OSError:\n")
    mentee_program.write("            print(\"Error - cannot open file \" + sys.argv[1] + \"'\")\n")
    mentee_program.close()


# This function will read in the csv file specified in the command line (if the file is valid),
# and provides hints to the user if there is anything wrong with the command line arguments.
if __name__ == '__main__':
    # If the amount of arguments (plus the name of the program) is not 2, we will inform the user.
    if len(sys.argv) != 2:
        print("Error - invalid number of arguments (must specify the training csv file)")

    else:
        try:
            # The second cmd argument is the csv file we have to open and retrieve data from
            with open(sys.argv[1]) as csv_file:
                read_data = csv.reader(csv_file)
                read_data.__next__()  # We ignore the headers
                records = []  # A list of all the records in the training data set
                all_splits = []  # Initialize the global list of splits to an empty array
                all_age = []  # Initialize the global list of ages to an empty array
                all_height = []  # Initialize the global list of heights to an empty array
                all_tail = []  # Initialize the global list of tail lengths to an empty array
                all_hair = []  # Initialize the global list of hair lengths to an empty array
                all_bang = []  # Initialize the global list of bang lengths to an empty array
                all_reach = []  # Initialize the global list of reaches to an empty array

                # Add each value of a record to a local list
                for record in read_data:
                    # We normalize each age by rounding them to the nearest 2 years
                    the_float = float(record[0].strip())
                    norm_age = round(the_float / 2) * 2
                    all_age.append(norm_age)  # Add the normalized value to the global list

                    # We normalize each height by rounding them to the nearest 4 centimeters
                    the_float = float(record[1].strip())
                    norm_height = round(the_float / 4) * 4
                    all_height.append(norm_height)  # Add the normalized value to the global list

                    # We normalize each tail length by rounding them to the nearest 2 units
                    the_float = float(record[2].strip())
                    norm_tail = round(the_float / 2) * 2
                    all_tail.append(norm_tail)  # Add the normalized value to the global list

                    # We normalize each hair length by rounding them to the nearest 2 units
                    the_float = float(record[3].strip())
                    norm_hair = round(the_float / 2) * 2
                    all_hair.append(norm_hair)  # Add the normalized value to the global list

                    # We normalize each bang length by rounding them to the nearest 2 units
                    the_float = float(record[4].strip())
                    norm_bang = round(the_float / 2) * 2
                    all_bang.append(norm_bang)  # Add the normalized value to the global list

                    # We normalize each reach by rounding them to the nearest 2 units
                    the_float = float(record[5].strip())
                    norm_reach = round(the_float / 2) * 2
                    all_reach.append(norm_reach)  # Add the normalized value to the global list

                    # We convert each lobe value into an int
                    lobe = int(record[6].strip())

                    # We convert each class id into an int
                    class_id = int(record[8].strip())

                    this_record = [norm_age, norm_height, norm_tail, norm_hair, norm_bang, norm_reach, lobe, class_id]
                    records.append(this_record)  # We add the normalized record to the record list

                # Runs the recursive function to find best ways to split
                best_split(records, 0)

                # Write a new trained program utilizing the results from best_split
                write_trained_program()

        # If the file is unable to be opened for whatever reason, we will inform the user.
        except OSError:
            print("Error - cannot open file '" + sys.argv[1] + "'")
