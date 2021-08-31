# MaxQuant

:link: *[Connecting to Compute Canada server](connect.md)*

#### Steps

* [Upload dataset files to Compute Canada](#upload-dataset-files-to-compute-canada)
* [Run MaxQuant](#run-maxquant)
* [Download results](#download-results)

## Upload dataset files to Compute Canada

See [Uploading dataset files to Compute Canada server](upload.md)

## Run MaxQuant

Run the following commands

```shell
module load maxquant
maxquant
```

This will add a job to run MaxQuant using `sbatch` with 1 CPU and 5 GB of memory per sample.

### Partial processing

If your MaxQuant job failed, check the output to find at which part of the job the process failed.

```shell
ls *.out
```

Look for the most recent `maxquant-?????.out` file. Then print its content using:

```shell
cat maxquant-?????.out
```

:memo: replace `maxquant-?????.out` with the real filename

To find the job id from which to start processing:

```shell
maxquant -n
```

:bulb: use a job id that is before the last job shown in the `maxquant-?????.out` file

To call MaxQuant starting from job id `18`, use this command:

```shell
maxquant -p 18
```

:memo: replace `18` with the actual job id to use

## Download results

Once you receive an email telling you that MaxQuant completed, you can download the results from the following folders
under `scratch/$dataset_name`

1. `combined/txt`
2. `combined/andromeda`

Use the same FTP program to download as for uploading, see [upload](upload.md)
