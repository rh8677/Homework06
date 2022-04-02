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
                output_file = open("output.csv", "w", newline="")  # Puts the classified data into another csv file
                write_data = csv.writer(output_file)
                header = next(read_data)
                header.append('Class')
                write_data.writerow(header)  # Puts the header in the output file
                for row in read_data:
                    the_float = float(row[0].strip())
                    rounded_num = round(the_float / 2) * 2

                    # If the normalized age is less than the number specified, it will belong in the Assam class
                    if rounded_num <= 46:
                        row.append('+1')
                        write_data.writerow(row)

                    # If the normalized age is greater than the number specified, it will belong in the Bhutan
                    # class instead
                    else:
                        row.append('-1')
                        write_data.writerow(row)
            csv_file.close()
            output_file.close()

        # If the file is unable to be opened for whatever reason, we will inform the user.
        except OSError:
            print("Error - cannot open file " + sys.argv[1] + "'")
