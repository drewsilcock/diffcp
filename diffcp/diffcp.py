import click
import os
from os import listdir
from os.path import isfile, isdir, basename


class CopyError(Exception):
    pass


def find_unique_files(first_folder, second_folder, verbose):
    """ Return the list of files which are present in `first_folder`, but not
    in `second_folder`. """

    if verbose:
        print "Identifying unique files..."

    unique_filenames = [f for f in listdir(first_folder)
                        if f not in listdir(second_folder)]

    if verbose:
        print "Successfully found unique files."

    unique_full_filenames = [first_folder + fn for fn in unique_filenames]

    return unique_full_filenames


def check_output_dir(directory):
    """ Check whether `directory` exists. If it doesn't, create it. """

    if isfile(directory):  # Should this be absolved into the try mkdir?
        print """\nError: '{}' is a file. Please choose another output \
                 directory name.""".format(directory)
        exit(1)

    if not isdir(directory):
        print "\nDirectory '{}' does not yet exist. Creating dir...".format(
            directory)
        try:
            os.mkdir(directory)
        except Exception as e:  # Find out the more specific error
            print "Error: Error creating output directory '{}'".format(
                directory)
            print "Exception: {}".format(e.__doc__)
            print "Error message: {}".format(e.message)
            exit(3)
        else:
            print "Successfully created dirctory '{}'.\n".format(directory)
    else:
        inp = raw_input("""\nDirectory '{}' already exists. \
                        \nDo you want to proceed? ['y', 'yes' or Enter] \
                        \n> """.format(directory))
        if inp.lower() not in ["", "yes", "y"]:
            print "Exiting..."
            exit(2)

    return True


def cp_files(filenames, directory, verbose):
    """ Copies all `filenames` into `directory`. """

    if verbose:
        print "\nCopying files into '{}'...".format(directory)

    for input_fn in filenames:
        with open(input_fn) as input_file:
            with open(directory + basename(input_fn), "w") as output_file:
                if verbose:
                    print "Copying file '{}'...".format(basename(input_fn))
                output_file.write(input_file.read())

    if verbose:
        print "Successfully copied files."

    return True


def diffcp(first_folder, second_folder, output_folder, verbose):
    """ Finds all files present in `first_folder` and not in `second_folder`,
    and copies them from `first_folder` into `output_folder`. """

    unique_files = find_unique_files(first_folder, second_folder, verbose)

    check_output_dir(output_folder)

    # Should I include `is True` here? What does PEP8 say?
    # In fact, maybe this check isn't necessary in the first place, since
    # errors in `cp_files` will be caught in that method...
    if cp_files(unique_files, output_folder, verbose) is True:
        print "\nAll unique files successfully copied into output directory."
    else:
        print "\nError copying unique files.\n"
        raise CopyError

    return True


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    version = 1.0
    click.echo("Currently version {}".format(version))
    ctx.exit()


@click.command()
@click.argument("first_folder")
@click.argument("second_folder")
@click.argument("output_folder")
@click.option("-v", "--verbose", is_flag=True,
              help="""Print additional information as unique files are \
                      identified and copied.""")
@click.option("-V", "--version", is_flag=True, callback=print_version,
              expose_value=False, is_eager=True, default=False)
def main(first_folder, second_folder, output_folder, verbose):
    """ Find all files in `first_folder` that don't have any corresponding
    files of the same filename in `second_folder`, and copying them into
    separate folder `output_folder`. Note that currently only filenames
    and not file contents are checked for equality. """

    return diffcp(first_folder, second_folder, output_folder, verbose)


if __name__ == "__main__":
    main()