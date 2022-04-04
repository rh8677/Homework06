import csv
import sys


# This function reads the csv file specified in the command line, and classifies each row of data into one of
# two classes.
if __name__ == '__main__':
    # If the amount of arguments (plus the name of the program) is not 2, we will inform the user.
    if len(sys.argv) != 2:
        print("Error - invalid number of arguments (must specify the csv file)")
    else:
        try:
            # The second cmd argument is the csv file we have to open and retrieve data from
            with open(sys.argv[1]) as csv_file:
                read_data = csv.reader(csv_file)
                all_records = []  # The normalized records that we will classify later
                output_file = open("output.csv", "w", newline="")  # Puts the classified data into another csv file
                write_data = csv.writer(output_file)
                header = next(read_data)
                header.append('Class')
                write_data.writerow(header)  # Puts the header in the output file

                # We first normalize values in each record
                for row in read_data:
                    cur_record = [0] * 7  # The record with normalized values

                    # Append the normalized age into the record array
                    the_float = float(row[0].strip())
                    norm_age = round(the_float / 2) * 2
                    cur_record[0] = norm_age

                    # Append the normalized height into the record array
                    the_float = float(row[1].strip())
                    norm_height = round(the_float / 4) * 4
                    cur_record[1] = norm_height

                    # Append the normalized tail length into the record array
                    the_float = float(row[2].strip())
                    norm_tail = round(the_float / 2) * 2
                    cur_record[2] = norm_tail

                    # Append the normalized hair length into the record array
                    the_float = float(row[3].strip())
                    norm_hair = round(the_float / 2) * 2
                    cur_record[3] = norm_hair

                    # Append the normalized bang length into the record array
                    the_float = float(row[4].strip())
                    norm_bang = round(the_float / 2) * 2
                    cur_record[4] = norm_bang

                    # Append the normalized reach into the record array
                    the_float = float(row[5].strip())
                    norm_reach = round(the_float / 2) * 2
                    cur_record[5] = norm_reach

                    # Append the earlobe values into the record array
                    earlobe = int(row[6].strip())
                    cur_record[6] = earlobe

                    all_records.append(cur_record)

                # For each record with normalized values, we determine which class it belongs to
                for record in all_records:
                    if record[3] <= 10:
                        if record[2] <= 4:
                            write_data.writerow(['1'])
                        else:
                            if record[0] <= 40:
                                if record[1] <= 136:
                                    write_data.writerow(['1'])
                                else:
                                    write_data.writerow(['-1'])
                            else:
                                if record[3] <= 8:
                                    write_data.writerow(['-1'])
                                else:
                                    write_data.writerow(['-1'])
                    else:
                        write_data.writerow(['1'])

            csv_file.close()
            output_file.close()

        # If the file is unable to be opened for whatever reason, we will inform the user.
        except OSError:
            print("Error - cannot open file " + sys.argv[1] + "'")
