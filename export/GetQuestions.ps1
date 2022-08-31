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

function GetQuestion {
    Param (
        $question_id
    )

    $method = "rest/questions/1.0/question"
    $url = "https://${domain}/${method}/${question_id}"

    $result = Invoke-RestMethod -Method Get -Uri $url -Headers $Headers -Credential $credential

    $result | ConvertTo-Json | Out-File "$location\questions\${question_id}.json"
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
New-Item -ItemType Directory -Path "${location}\questions"

GetQuestions
