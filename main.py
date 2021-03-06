# Raymond Hu 4/2/22
import csv
import math
import sys

all_splits = []  # A list of all the splits (attribute and threshold) that happens within the ideal decision tree
attr_array = []  # A list of lists of all the attributes that are relevant for the given data
total_depth = 0  # The total amount of levels for the decision tree


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
# argument 2 (index_split) - the index of the decision tree level that we append some info into
def best_split(the_records, depth, index_split):
    major_class = more_class(the_records)  # The class that appears more frequently in the records
    major_percent = more_percent(the_records)  # The percentage of the major_class
    global total_depth

    # Update the global max depth if the local depth is greater than it
    if depth + 1 > total_depth:
        total_depth = depth + 1

    # If the decision tree already has 9 levels, or there are less than 9 records, or if the percentage
    # of the majority class is greater than 95 percent, we will stop splitting
    if depth > 10 or len(the_records) < 9 or major_percent > 0.95:

        # If the stopping criteria is met, we let the program know there is no need to split anymore
        all_splits[depth][index_split] = [0, 0, major_class]

        return
    else:
        best_attribute = 0  # We initialize the best attribute to be the age
        best_threshold = min(attr_array[0])  # We initialize the best attribute to be the min threshold of age
        best_entropy = 1  # We initialize the best weighted entropy to be the worst possible
        list_counter = 0  # We use this counter to determine the index belonging to the current attribute

        # For each attribute list in the global array
        for attr_list in attr_array:
            local_best_ent = 1  # We initialize the best entropy for this attribute
            local_best_thr = min(attr_list)  # We initialize the best threshold
            current_threshold = min(attr_list)  # We keep track of the current threshold

            # We go over every possible threshold for the attribute list
            while current_threshold <= max(attr_list):
                node1 = []
                node2 = []
                for a_record in the_records:
                    # If the attribute of the record is less than or equal to the test threshold, it
                    # will go into the first list
                    if a_record[list_counter] <= current_threshold:
                        node1.append(a_record)
                    else:
                        node2.append(a_record)

                # The weighted entropy = (length of first list / total records) x entropy of first list +
                # (length of second list / total records) x entropy of second list)
                wei_entropy = ((len(node1) / len(the_records)) * cal_entropy(node1)) + ((len(node2) / len(the_records))
                                                                                        * cal_entropy(node2))

                # If the weighted entropy of this threshold is better than the previous best, we
                # update the appropriate values to reflect this
                if wei_entropy < local_best_ent:
                    local_best_ent = wei_entropy
                    local_best_thr = current_threshold

                current_threshold += 1  # Test new threshold

            # If the best entropy of the current attribute is better than the global entropy, we
            # update the appropriate values to reflect this
            if local_best_ent < best_entropy:
                best_attribute = list_counter
                best_threshold = local_best_thr
                best_entropy = local_best_ent

            list_counter += 1  # Update new attribute index

    split1 = []  # The list of records in the first split
    split2 = []  # The list of records in the second split

    # We append each record to either the first or second split according to the best attribute and
    # its best threshold
    for test_record in the_records:
        if test_record[best_attribute] <= best_threshold:
            split1.append(test_record)
        else:
            split2.append(test_record)

    # We append the best attribute, threshold, and the class that appears the most to the global list
    # for the classifier program
    all_splits[depth][index_split] = [best_attribute, best_threshold, major_class]

    best_split(split1, depth + 1, index_split * 2)  # Perform a recursive call using the first split
    best_split(split2, depth + 1, (index_split * 2) + 1)  # Perform a recursive call using the second split


# This function will build a trained program (a python file called 'HW05_Classifier_Hu.py') which will
# utilize the decision tree built by best_split in order to determine which class each record of a csv
# file falls into.
def write_trained_program():
    print(total_depth)
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
    mentee_program.write("                all_records = []  # The normalized records that we will classify later\n")
    mentee_program.write("                output_file = open(\"output.csv\", \"w\", newline=\"\")  # Puts the "
                         "classified data into another csv file\n")
    mentee_program.write("                write_data = csv.writer(output_file)\n")
    mentee_program.write("                header = next(read_data)\n")
    mentee_program.write("                header.append('Class')\n")
    mentee_program.write("                write_data.writerow(header)  # Puts the header in the output file\n")
    mentee_program.write("\n")
    mentee_program.write("                # We first normalize values in each record\n")
    mentee_program.write("                for row in read_data:\n")
    mentee_program.write("                    cur_record = [0] * 7  # The record with normalized values\n")
    mentee_program.write("\n")
    mentee_program.write("                    # Append the normalized age into the record array\n")
    mentee_program.write("                    the_float = float(row[0].strip())\n")
    mentee_program.write("                    norm_age = round(the_float / 2) * 2\n")
    mentee_program.write("                    cur_record[0] = norm_age\n")
    mentee_program.write("\n")
    mentee_program.write("                    # Append the normalized height into the record array\n")
    mentee_program.write("                    the_float = float(row[1].strip())\n")
    mentee_program.write("                    norm_height = round(the_float / 4) * 4\n")
    mentee_program.write("                    cur_record[1] = norm_height\n")
    mentee_program.write("\n")
    mentee_program.write("                    # Append the normalized tail length into the record array\n")
    mentee_program.write("                    the_float = float(row[2].strip())\n")
    mentee_program.write("                    norm_tail = round(the_float / 2) * 2\n")
    mentee_program.write("                    cur_record[2] = norm_tail\n")
    mentee_program.write("\n")
    mentee_program.write("                    # Append the normalized hair length into the record array\n")
    mentee_program.write("                    the_float = float(row[3].strip())\n")
    mentee_program.write("                    norm_hair = round(the_float / 2) * 2\n")
    mentee_program.write("                    cur_record[3] = norm_hair\n")
    mentee_program.write("\n")
    mentee_program.write("                    # Append the normalized bang length into the record array\n")
    mentee_program.write("                    the_float = float(row[4].strip())\n")
    mentee_program.write("                    norm_bang = round(the_float / 2) * 2\n")
    mentee_program.write("                    cur_record[4] = norm_bang\n")
    mentee_program.write("\n")
    mentee_program.write("                    # Append the normalized reach into the record array\n")
    mentee_program.write("                    the_float = float(row[5].strip())\n")
    mentee_program.write("                    norm_reach = round(the_float / 2) * 2\n")
    mentee_program.write("                    cur_record[5] = norm_reach\n")
    mentee_program.write("\n")
    mentee_program.write("                    # Append the earlobe values into the record array\n")
    mentee_program.write("                    earlobe = int(row[6].strip())\n")
    mentee_program.write("                    cur_record[6] = earlobe\n")
    mentee_program.write("\n")
    mentee_program.write("                    all_records.append(cur_record)\n")
    mentee_program.write("\n")
    mentee_program.write("                # For each record with normalized values, we determine which class it "
                         "belongs to\n")
    mentee_program.write("                for record in all_records:\n")

    # This is if the decision tree is only 1 level deep
    if total_depth == 1:
        mentee_program.write("write_data.writerow(['" + str(all_splits[0][0][2]) + "'])\n")

    # This is if the decision tree is 2 levels deep
    elif total_depth == 2:
        mentee_program.write("                    if record[" + str(all_splits[0][0][0]) + "] <= " +
                             str(all_splits[0][0][1]) + ":\n")
        mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][0][2]) + "'])\n")
        mentee_program.write("                    else:\n")
        mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][1][2]) + "'])\n")

    # This is if the decision tree is 3 levels deep
    elif total_depth == 3:
        mentee_program.write("                    if record[" + str(all_splits[0][0][0]) + "] <= " +
                             str(all_splits[0][0][1]) + ":\n")

        # If the stopping criteria has been met, we just return whatever majority class exists for this node
        if all_splits[1][0][1] == 0:
            mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][0][2]) + "'])\n")

            # Otherwise, we utilize the best attribute and the best threshold
        else:
            mentee_program.write("                        if record[" + str(all_splits[1][0][0]) + "] <= " +
                                 str(all_splits[1][0][1]) + ":\n")
            mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][0][2]) +
                                 "'])\n")
            mentee_program.write("                        else:\n")
            mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][1][2]) +
                                 "'])\n")
        mentee_program.write("                    else:\n")

        # If the stopping criteria has been met, we just return whatever majority class exists for this node
        if all_splits[1][1][1] == 0:
            mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][1][2]) + "'])\n")

        # Otherwise, we utilize the best attribute and the best threshold
        else:
            mentee_program.write("                        if record[" + str(all_splits[1][1][0]) + "] <= " +
                                 str(all_splits[1][1][1]) + ":\n")
            mentee_program.write(
                "                            write_data.writerow(['" + str(all_splits[2][2][2]) + "'])\n")
            mentee_program.write("                        else:\n")
            mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][3][2]) +
                                 "'])\n")

    # This is if the decision tree is 4 levels deep
    elif total_depth == 4:
        mentee_program.write("                    if record[" + str(all_splits[0][0][0]) + "] <= " +
                             str(all_splits[0][0][1]) + ":\n")

        # If the stopping criteria has been met, we just return whatever majority class exists for this node
        if all_splits[1][0][1] == 0:
            mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][0][2]) + "'])\n")

            # Otherwise, we utilize the best attribute and the best threshold
        else:
            mentee_program.write("                        if record[" + str(all_splits[1][0][0]) + "] <= " +
                                 str(all_splits[1][0][1]) + ":\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][0][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][0][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][0][0]) + "] <= " +
                                     str(all_splits[2][0][1]) + ":\n")
                mentee_program.write("                                write_data.writerow(['" +
                                     str(all_splits[3][0][2]) + "'])\n")
                mentee_program.write("                            else:\n")
                mentee_program.write("                                write_data.writerow(['" +
                                     str(all_splits[3][1][2]) + "'])\n")
            mentee_program.write("                        else:\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][1][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][1][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][1][0]) + "] <= " +
                                     str(all_splits[2][1][1]) + ":\n")
                mentee_program.write("                                write_data.writerow(['" +
                                     str(all_splits[3][2][2]) + "'])\n")
                mentee_program.write("                            else:\n")
                mentee_program.write("                                write_data.writerow(['" +
                                     str(all_splits[3][3][2]) + "'])\n")

        mentee_program.write("                    else:\n")

        # If the stopping criteria has been met, we just return whatever majority class exists for this node
        if all_splits[1][1][1] == 0:
            mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][1][2]) + "'])\n")

            # Otherwise, we utilize the best attribute and the best threshold
        else:
            mentee_program.write("                        if record[" + str(all_splits[1][1][0]) + "] <= " +
                                 str(all_splits[1][0][1]) + ":\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][2][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][2][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][2][0]) + "] <= " +
                                     str(all_splits[2][2][1]) + ":\n")
                mentee_program.write("                                write_data.writerow(['" +
                                     str(all_splits[3][5][2]) + "'])\n")
                mentee_program.write("                            else:\n")
                mentee_program.write("                                write_data.writerow(['" +
                                     str(all_splits[3][6][2]) + "'])\n")
            mentee_program.write("                        else:\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][3][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][3][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][3][0]) + "] <= " +
                                     str(all_splits[2][3][1]) + ":\n")
                mentee_program.write("                                write_data.writerow(['" +
                                     str(all_splits[3][6][2]) + "'])\n")
                mentee_program.write("                            else:\n")
                mentee_program.write("                                write_data.writerow(['" +
                                     str(all_splits[3][7][2]) + "'])\n")

    # This is if the decision tree is 5 levels deep
    elif total_depth == 5:
        mentee_program.write("                    if record[" + str(all_splits[0][0][0]) + "] <= " +
                             str(all_splits[0][0][1]) + ":\n")

        # If the stopping criteria has been met, we just return whatever majority class exists for this node
        if all_splits[1][0][1] == 0:
            mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][0][2]) + "'])\n")

        # Otherwise, we utilize the best attribute and the best threshold
        else:
            mentee_program.write("                        if record[" + str(all_splits[1][0][0]) + "] <= " +
                                 str(all_splits[1][0][1]) + ":\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][0][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][0][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][0][0]) + "] <= " +
                                     str(all_splits[2][0][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][0][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][0][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][0][0]) +
                                         "] <= " + str(all_splits[3][0][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][0][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][1][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][1][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][1][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][1][0]) +
                                         "] <= " + str(all_splits[3][1][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][2][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][3][2]) + "'])\n")

            mentee_program.write("                        else:\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][1][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][1][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][1][0]) + "] <= " +
                                     str(all_splits[2][1][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][2][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][2][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][2][0]) +
                                         "] <= " + str(all_splits[3][2][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][4][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][5][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][3][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][3][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][3][0]) +
                                         "] <= " + str(all_splits[3][3][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][6][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][7][2]) + "'])\n")

        mentee_program.write("                    else:\n")

        # If the stopping criteria has been met, we just return whatever majority class exists for this node
        if all_splits[1][1][1] == 0:
            mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][1][2]) + "'])\n")

        # Otherwise, we utilize the best attribute and the best threshold
        else:
            mentee_program.write("                        if record[" + str(all_splits[1][1][0]) + "] <= " +
                                 str(all_splits[1][1][1]) + ":\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][2][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][2][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][2][0]) + "] <= " +
                                     str(all_splits[2][2][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][4][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][4][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][4][0]) +
                                         "] <= " + str(all_splits[3][4][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][8][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][9][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][5][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][5][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][5][0]) +
                                         "] <= " + str(all_splits[3][5][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][10][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][11][2]) + "'])\n")

            mentee_program.write("                        else:\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][3][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][3][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][3][0]) + "] <= " +
                                     str(all_splits[2][3][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][6][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][6][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][6][0]) +
                                         "] <= " + str(all_splits[3][6][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][12][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][13][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][7][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][7][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][7][0]) +
                                         "] <= " + str(all_splits[3][7][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][14][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][15][2]) + "'])\n")

    # This is if the decision tree is 6 levels deep
    elif total_depth == 6:
        mentee_program.write("                    if record[" + str(all_splits[0][0][0]) + "] <= " +
                             str(all_splits[0][0][1]) + ":\n")

        # If the stopping criteria has been met, we just return whatever majority class exists for this node
        if all_splits[1][0][1] == 0:
            mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][0][2]) + "'])\n")

        # Otherwise, we utilize the best attribute and the best threshold
        else:
            mentee_program.write("                        if record[" + str(all_splits[1][0][0]) + "] <= " +
                                 str(all_splits[1][0][1]) + ":\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][0][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][0][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][0][0]) + "] <= " +
                                     str(all_splits[2][0][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][0][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][0][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][0][0]) +
                                         "] <= " + str(all_splits[3][0][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][0][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][1][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][1][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][1][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][1][0]) +
                                         "] <= " + str(all_splits[3][1][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][2][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][3][2]) + "'])\n")

            mentee_program.write("                        else:\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][1][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][1][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][1][0]) + "] <= " +
                                     str(all_splits[2][1][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][2][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][2][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][2][0]) +
                                         "] <= " + str(all_splits[3][2][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][4][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][5][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][3][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][3][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][3][0]) +
                                         "] <= " + str(all_splits[3][3][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][6][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][7][2]) + "'])\n")

        mentee_program.write("                    else:\n")

        # If the stopping criteria has been met, we just return whatever majority class exists for this node
        if all_splits[1][1][1] == 0:
            mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][1][2]) + "'])\n")

        # Otherwise, we utilize the best attribute and the best threshold
        else:
            mentee_program.write("                        if record[" + str(all_splits[1][1][0]) + "] <= " +
                                 str(all_splits[1][1][1]) + ":\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][2][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][2][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][2][0]) + "] <= " +
                                     str(all_splits[2][2][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][4][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][4][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][4][0]) +
                                         "] <= " + str(all_splits[3][4][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][8][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][9][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][5][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][5][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][5][0]) +
                                         "] <= " + str(all_splits[3][5][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][10][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][11][2]) + "'])\n")

            mentee_program.write("                        else:\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][3][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][3][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][3][0]) + "] <= " +
                                     str(all_splits[2][3][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][6][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][6][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][6][0]) +
                                         "] <= " + str(all_splits[3][6][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][12][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][13][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][7][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][7][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][7][0]) +
                                         "] <= " + str(all_splits[3][7][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][14][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][15][2]) + "'])\n")

    # This is if the decision tree is 7 levels deep
    elif total_depth == 7:
        mentee_program.write("                    if record[" + str(all_splits[0][0][0]) + "] <= " +
                             str(all_splits[0][0][1]) + ":\n")

        # If the stopping criteria has been met, we just return whatever majority class exists for this node
        if all_splits[1][0][1] == 0:
            mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][0][2]) + "'])\n")

        # Otherwise, we utilize the best attribute and the best threshold
        else:
            mentee_program.write("                        if record[" + str(all_splits[1][0][0]) + "] <= " +
                                 str(all_splits[1][0][1]) + ":\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][0][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][0][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][0][0]) + "] <= " +
                                     str(all_splits[2][0][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][0][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][0][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][0][0]) +
                                         "] <= " + str(all_splits[3][0][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][0][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][1][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][1][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][1][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][1][0]) +
                                         "] <= " + str(all_splits[3][1][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][2][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][3][2]) + "'])\n")

            mentee_program.write("                        else:\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][1][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][1][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][1][0]) + "] <= " +
                                     str(all_splits[2][1][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][2][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][2][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][2][0]) +
                                         "] <= " + str(all_splits[3][2][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][4][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][5][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][3][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][3][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][3][0]) +
                                         "] <= " + str(all_splits[3][3][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][6][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][7][2]) + "'])\n")

        mentee_program.write("                    else:\n")

        # If the stopping criteria has been met, we just return whatever majority class exists for this node
        if all_splits[1][1][1] == 0:
            mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][1][2]) + "'])\n")

        # Otherwise, we utilize the best attribute and the best threshold
        else:
            mentee_program.write("                        if record[" + str(all_splits[1][1][0]) + "] <= " +
                                 str(all_splits[1][1][1]) + ":\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][2][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][2][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][2][0]) + "] <= " +
                                     str(all_splits[2][2][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][4][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][4][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][4][0]) +
                                         "] <= " + str(all_splits[3][4][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][8][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][9][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][5][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][5][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][5][0]) +
                                         "] <= " + str(all_splits[3][5][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][10][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][11][2]) + "'])\n")

            mentee_program.write("                        else:\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][3][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][3][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][3][0]) + "] <= " +
                                     str(all_splits[2][3][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][6][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][6][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][6][0]) +
                                         "] <= " + str(all_splits[3][6][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][12][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][13][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][7][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][7][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][7][0]) +
                                         "] <= " + str(all_splits[3][7][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][14][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][15][2]) + "'])\n")

    # This is if the decision tree is 8 levels deep
    elif total_depth == 8:
        mentee_program.write("                    if record[" + str(all_splits[0][0][0]) + "] <= " +
                             str(all_splits[0][0][1]) + ":\n")

        # If the stopping criteria has been met, we just return whatever majority class exists for this node
        if all_splits[1][0][1] == 0:
            mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][0][2]) + "'])\n")

        # Otherwise, we utilize the best attribute and the best threshold
        else:
            mentee_program.write("                        if record[" + str(all_splits[1][0][0]) + "] <= " +
                                 str(all_splits[1][0][1]) + ":\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][0][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][0][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][0][0]) + "] <= " +
                                     str(all_splits[2][0][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][0][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][0][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][0][0]) +
                                         "] <= " + str(all_splits[3][0][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][0][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][1][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][1][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][1][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][1][0]) +
                                         "] <= " + str(all_splits[3][1][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][2][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][3][2]) + "'])\n")

            mentee_program.write("                        else:\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][1][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][1][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][1][0]) + "] <= " +
                                     str(all_splits[2][1][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][2][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][2][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][2][0]) +
                                         "] <= " + str(all_splits[3][2][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][4][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][5][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][3][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][3][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][3][0]) +
                                         "] <= " + str(all_splits[3][3][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][6][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][7][2]) + "'])\n")

        mentee_program.write("                    else:\n")

        # If the stopping criteria has been met, we just return whatever majority class exists for this node
        if all_splits[1][1][1] == 0:
            mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][1][2]) + "'])\n")

        # Otherwise, we utilize the best attribute and the best threshold
        else:
            mentee_program.write("                        if record[" + str(all_splits[1][1][0]) + "] <= " +
                                 str(all_splits[1][1][1]) + ":\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][2][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][2][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][2][0]) + "] <= " +
                                     str(all_splits[2][2][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][4][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][4][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][4][0]) +
                                         "] <= " + str(all_splits[3][4][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][8][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][9][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][5][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][5][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][5][0]) +
                                         "] <= " + str(all_splits[3][5][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][10][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][11][2]) + "'])\n")

            mentee_program.write("                        else:\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][3][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][3][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][3][0]) + "] <= " +
                                     str(all_splits[2][3][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][6][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][6][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][6][0]) +
                                         "] <= " + str(all_splits[3][6][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][12][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][13][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][7][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][7][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][7][0]) +
                                         "] <= " + str(all_splits[3][7][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][14][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][15][2]) + "'])\n")

    # This is if the decision tree is 9 levels deep
    elif total_depth == 9:
        mentee_program.write("                    if record[" + str(all_splits[0][0][0]) + "] <= " +
                             str(all_splits[0][0][1]) + ":\n")

        # If the stopping criteria has been met, we just return whatever majority class exists for this node
        if all_splits[1][0][1] == 0:
            mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][0][2]) + "'])\n")

        # Otherwise, we utilize the best attribute and the best threshold
        else:
            mentee_program.write("                        if record[" + str(all_splits[1][0][0]) + "] <= " +
                                 str(all_splits[1][0][1]) + ":\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][0][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][0][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][0][0]) + "] <= " +
                                     str(all_splits[2][0][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][0][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][0][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][0][0]) +
                                         "] <= " + str(all_splits[3][0][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][0][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][1][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][1][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][1][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][1][0]) +
                                         "] <= " + str(all_splits[3][1][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][2][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][3][2]) + "'])\n")

            mentee_program.write("                        else:\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][1][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][1][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][1][0]) + "] <= " +
                                     str(all_splits[2][1][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][2][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][2][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][2][0]) +
                                         "] <= " + str(all_splits[3][2][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][4][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][5][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][3][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][3][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][3][0]) +
                                         "] <= " + str(all_splits[3][3][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][6][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][7][2]) + "'])\n")

        mentee_program.write("                    else:\n")

        # If the stopping criteria has been met, we just return whatever majority class exists for this node
        if all_splits[1][1][1] == 0:
            mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][1][2]) + "'])\n")

        # Otherwise, we utilize the best attribute and the best threshold
        else:
            mentee_program.write("                        if record[" + str(all_splits[1][1][0]) + "] <= " +
                                 str(all_splits[1][1][1]) + ":\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][2][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][2][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][2][0]) + "] <= " +
                                     str(all_splits[2][2][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][4][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][4][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][4][0]) +
                                         "] <= " + str(all_splits[3][4][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][8][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][9][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][5][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][5][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][5][0]) +
                                         "] <= " + str(all_splits[3][5][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][10][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][11][2]) + "'])\n")

            mentee_program.write("                        else:\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][3][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][3][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][3][0]) + "] <= " +
                                     str(all_splits[2][3][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][6][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][6][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][6][0]) +
                                         "] <= " + str(all_splits[3][6][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][12][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][13][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][7][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][7][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][7][0]) +
                                         "] <= " + str(all_splits[3][7][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][14][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][15][2]) + "'])\n")

    # This is if the decision tree is 10 levels deep
    elif total_depth == 10:
        mentee_program.write("                    if record[" + str(all_splits[0][0][0]) + "] <= " +
                             str(all_splits[0][0][1]) + ":\n")

        # If the stopping criteria has been met, we just return whatever majority class exists for this node
        if all_splits[1][0][1] == 0:
            mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][0][2]) + "'])\n")

        # Otherwise, we utilize the best attribute and the best threshold
        else:
            mentee_program.write("                        if record[" + str(all_splits[1][0][0]) + "] <= " +
                                 str(all_splits[1][0][1]) + ":\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][0][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][0][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][0][0]) + "] <= " +
                                     str(all_splits[2][0][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][0][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][0][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][0][0]) +
                                         "] <= " + str(all_splits[3][0][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][0][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][1][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][1][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][1][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][1][0]) +
                                         "] <= " + str(all_splits[3][1][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][2][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][3][2]) + "'])\n")

            mentee_program.write("                        else:\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][1][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][1][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][1][0]) + "] <= " +
                                     str(all_splits[2][1][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][2][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][2][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][2][0]) +
                                         "] <= " + str(all_splits[3][2][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][4][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][5][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][3][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][3][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][3][0]) +
                                         "] <= " + str(all_splits[3][3][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][6][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][7][2]) + "'])\n")

        mentee_program.write("                    else:\n")

        # If the stopping criteria has been met, we just return whatever majority class exists for this node
        if all_splits[1][1][1] == 0:
            mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][1][2]) + "'])\n")

        # Otherwise, we utilize the best attribute and the best threshold
        else:
            mentee_program.write("                        if record[" + str(all_splits[1][1][0]) + "] <= " +
                                 str(all_splits[1][1][1]) + ":\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][2][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][2][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][2][0]) + "] <= " +
                                     str(all_splits[2][2][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][4][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][4][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][4][0]) +
                                         "] <= " + str(all_splits[3][4][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][8][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][9][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][5][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][5][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][5][0]) +
                                         "] <= " + str(all_splits[3][5][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][10][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][11][2]) + "'])\n")

            mentee_program.write("                        else:\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][3][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][3][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][3][0]) + "] <= " +
                                     str(all_splits[2][3][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][6][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][6][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][6][0]) +
                                         "] <= " + str(all_splits[3][6][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][12][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][13][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][7][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][7][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][7][0]) +
                                         "] <= " + str(all_splits[3][7][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][14][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][15][2]) + "'])\n")

    # This is if the decision tree is 11 levels deep
    elif total_depth == 11:
        mentee_program.write("                    if record[" + str(all_splits[0][0][0]) + "] <= " +
                             str(all_splits[0][0][1]) + ":\n")

        # If the stopping criteria has been met, we just return whatever majority class exists for this node
        if all_splits[1][0][1] == 0:
            mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][0][2]) + "'])\n")

        # Otherwise, we utilize the best attribute and the best threshold
        else:
            mentee_program.write("                        if record[" + str(all_splits[1][0][0]) + "] <= " +
                                 str(all_splits[1][0][1]) + ":\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][0][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][0][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][0][0]) + "] <= " +
                                     str(all_splits[2][0][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][0][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][0][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][0][0]) +
                                         "] <= " + str(all_splits[3][0][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][0][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][1][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][1][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][1][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][1][0]) +
                                         "] <= " + str(all_splits[3][1][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][2][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][3][2]) + "'])\n")

            mentee_program.write("                        else:\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][1][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][1][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][1][0]) + "] <= " +
                                     str(all_splits[2][1][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][2][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][2][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][2][0]) +
                                         "] <= " + str(all_splits[3][2][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][4][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][5][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][3][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][3][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][3][0]) +
                                         "] <= " + str(all_splits[3][3][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][6][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][7][2]) + "'])\n")

        mentee_program.write("                    else:\n")

        # If the stopping criteria has been met, we just return whatever majority class exists for this node
        if all_splits[1][1][1] == 0:
            mentee_program.write("                        write_data.writerow(['" + str(all_splits[1][1][2]) + "'])\n")

        # Otherwise, we utilize the best attribute and the best threshold
        else:
            mentee_program.write("                        if record[" + str(all_splits[1][1][0]) + "] <= " +
                                 str(all_splits[1][1][1]) + ":\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][2][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][2][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][2][0]) + "] <= " +
                                     str(all_splits[2][2][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][4][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][4][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][4][0]) +
                                         "] <= " + str(all_splits[3][4][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][8][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][9][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][5][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][5][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][5][0]) +
                                         "] <= " + str(all_splits[3][5][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][10][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][11][2]) + "'])\n")

            mentee_program.write("                        else:\n")

            # If the stopping criteria has been met, we just return whatever majority class exists for this node
            if all_splits[2][3][1] == 0:
                mentee_program.write("                            write_data.writerow(['" + str(all_splits[2][3][2]) +
                                     "'])\n")

            else:
                mentee_program.write("                            if record[" + str(all_splits[2][3][0]) + "] <= " +
                                     str(all_splits[2][3][1]) + ":\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][6][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][6][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][6][0]) +
                                         "] <= " + str(all_splits[3][6][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][12][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][13][2]) + "'])\n")

                mentee_program.write("                            else:\n")

                # If the stopping criteria has been met, we just return whatever majority class exists for this node
                if all_splits[3][7][1] == 0:
                    mentee_program.write("                                write_data.writerow(['" +
                                         str(all_splits[3][7][2]) + "'])\n")

                # Otherwise, we utilize the best attribute and the best threshold
                else:
                    mentee_program.write("                                if record[" + str(all_splits[3][7][0]) +
                                         "] <= " + str(all_splits[3][7][1]) + ":\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][14][2]) + "'])\n")
                    mentee_program.write("                                else:\n")
                    mentee_program.write("                                    write_data.writerow(['" +
                                         str(all_splits[4][15][2]) + "'])\n")

    mentee_program.write("\n")
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
                level1 = [[0, 0, 0]]
                level2 = [[0, 0, 0]] * 2
                level3 = [[0, 0, 0]] * 4
                level4 = [[0, 0, 0]] * 8
                level5 = [[0, 0, 0]] * 16
                level6 = [[0, 0, 0]] * 32
                level7 = [[0, 0, 0]] * 64
                level8 = [[0, 0, 0]] * 128
                level9 = [[0, 0, 0]] * 256
                level10 = [[0, 0, 0]] * 512
                level11 = [[0, 0, 0]] * 1024
                total_depth = 0

                # Initialize the global list of splits to an empty array
                all_splits = [level1, level2, level3, level4, level5, level6, level7, level8, level9, level10, level11]
                attr_array = [[]] * 6  # Initialize all arrays to an empty array

                # Add each value of a record to a local list
                for record in read_data:
                    # We normalize each age by rounding them to the nearest 2 years
                    the_float = float(record[0].strip())
                    norm_age = round(the_float / 2) * 2

                    # Add the normalized value to the appropriate index of the list
                    if not attr_array[0]:
                        attr_array[0] = [norm_age]
                    else:
                        attr_array[0].append(norm_age)

                    # We normalize each height by rounding them to the nearest 4 centimeters
                    the_float = float(record[1].strip())
                    norm_height = round(the_float / 4) * 4

                    # Add the normalized value to the appropriate index of the list
                    if not attr_array[1]:
                        attr_array[1] = [norm_height]
                    else:
                        attr_array[1].append(norm_height)

                    # We normalize each tail length by rounding them to the nearest 2 units
                    the_float = float(record[2].strip())
                    norm_tail = round(the_float / 2) * 2

                    # Add the normalized value to the appropriate index of the list
                    if not attr_array[1]:
                        attr_array[2] = [norm_tail]
                    else:
                        attr_array[2].append(norm_tail)

                    # We normalize each hair length by rounding them to the nearest 2 units
                    the_float = float(record[3].strip())
                    norm_hair = round(the_float / 2) * 2

                    # Add the normalized value to the appropriate index of the list
                    if not attr_array[1]:
                        attr_array[3] = [norm_hair]
                    else:
                        attr_array[3].append(norm_hair)

                    # We normalize each bang length by rounding them to the nearest 2 units
                    the_float = float(record[4].strip())
                    norm_bang = round(the_float / 2) * 2

                    # Add the normalized value to the appropriate index of the list
                    if not attr_array[1]:
                        attr_array[4] = [norm_bang]
                    else:
                        attr_array[4].append(norm_bang)

                    # We normalize each reach by rounding them to the nearest 2 units
                    the_float = float(record[5].strip())
                    norm_reach = round(the_float / 2) * 2

                    # Add the normalized value to the appropriate index of the list
                    if not attr_array[1]:
                        attr_array[5] = [norm_reach]
                    else:
                        attr_array[5].append(norm_reach)

                    # We convert each lobe value into an int
                    lobe = int(record[6].strip())

                    # We convert each class id into an int
                    class_id = int(record[8].strip())

                    this_record = [norm_age, norm_height, norm_tail, norm_hair, norm_bang, norm_reach, lobe, class_id]
                    records.append(this_record)  # We add the normalized record to the record list

                # Runs the recursive function to find best ways to split
                best_split(records, 0, 0)

                # Prints out all levels of the decision tree so we know where we are splitting and where we aren't
                print(all_splits[0])
                print(all_splits[1])
                print(all_splits[2])
                print(all_splits[3])
                print(all_splits[4])
                print(all_splits[5])
                print(all_splits[6])
                print(all_splits[7])
                print(all_splits[8])
                print(all_splits[9])
                print(all_splits[10])

                # Write a new trained program utilizing the results from best_split
                write_trained_program()

        # If the file is unable to be opened for whatever reason, we will inform the user.
        except OSError:
            print("Error - cannot open file '" + sys.argv[1] + "'")
