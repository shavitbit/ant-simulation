# use this function to generate ids. To generate 5 ids:
# .\jobsID-gen.ps1 gen-id 5
function Gen-ID {
    param (
        [int]$numOfId
    )

    for ($i = 1; $i -le $numOfId; $i++) {
        $antid = "{0:F1}-{1:F1}-{2:F1}-{3:F1}" -f 
            (Get-Random -Minimum 0.1 -Maximum 100),
            (Get-Random -Minimum 0.1 -Maximum 150),
            (Get-Random -Minimum 0.1 -Maximum 100),
            (Get-Random -Minimum 0 -Maximum 30)

        $id += '"'+$antid+'" ' 
    }
        write-host $id
}

# Check if the script is called with arguments
if ($args.Count -eq 2 -and $args[0] -eq "Gen-ID") {
    Gen-ID -numOfId $args[1]
}