# get all questions and answers from Confluence Questions
# see https://docs.atlassian.com/confluence-questions/rest/resource_QuestionResource.html#path__question.html

$domain = "confluence.example.org"
$user = 'administrator'
$pass = 'topsecret'

# see https://stackoverflow.com/a/27951845
$pair = "$($user):$($pass)"
$encodedCreds = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes($pair))
$basicAuthValue = "Basic $encodedCreds"
$Headers = @{
    Authorization = $basicAuthValue
}

# see https://stackoverflow.com/a/30203972/1632368
$secpasswd = ConvertTo-SecureString $pass -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential($user, $secpasswd)

function DownloadAttachment {
    Param (
        $question_id
        $path
    }

Write-Host $path
    $filename = $path.Substring(0, $path.IndexOf("?"))
    $filename = $path.Substring($path.LastIndexOf("/") + 1)
Write-Host $filename

    New-Item -ItemType Directory -Path "${location}\questions\${question_id}" -Force
    $parameters = @{
        Uri = "https://${domain}${path}"
        Method = "GET"
        Headers = $Headers
        Credential = $credential
        OutFile = "${location}\questions\${question_id}\$filename}"
    }

    Invoke-WebRequest @parameters
}

function GetQuestion {
    Param (
        $question_id
    )

    $method = "rest/questions/1.0/question"
    $url = "https://${domain}/${method}/${question_id}"

    $result = Invoke-RestMethod -Method Get -Uri $url -Headers $Headers -Credential $credential

    $content = $result | ConvertTo-Json
    $content | Out-File "$location\questions\${question_id}.json"

    # also download the attachments
    if ($content -match "/download/attachments/") {
        $index = $content.IndexOf("/download/attachments/")
        while ($index -gt 0) {
            $closingQuote = $content.IndexOf("\\\"", $index)
            $path = $content.Substring($index, $closingQuote - $index)
            DownloadAttachment $question_id $path

            $index = $content.IndexOf("/download/attachments/", $closingQuote)
        }
    }
}

function GetQuestions {

    Param (
        $start = 0,
        $limit = 100
    )

    $method = "rest/questions/1.0/question"
    $url = "https://${domain}/${method}?start=${start}&limit=$limit"

    $result = Invoke-RestMethod -Method Get -Uri $url -Headers $Headers -Credential $credential

    $count = 0
    foreach ($question in $result) {
        $count += 1
        GetQuestion $question.id
    }

    if ($count -eq $limit) {
        GetQuestions ($start + $limit) $limit
    }
}

$location = Get-Location
New-Item -ItemType Directory -Path "${location}\questions" -Force

GetQuestions
