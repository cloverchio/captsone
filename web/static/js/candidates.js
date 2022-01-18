// too lazy for fancy es6 map filter stuff...

var checkboxName = 'candidate_checkbox';

function toggleSelect() {
  var checkboxes = document.getElementsByName(checkboxName);
  for (var i = 0; i < checkboxes.length; i++) {
    var checkbox = checkboxes[i];
    if (checkbox.checked) {
        checkbox.checked = false;
    } else {
        checkbox.checked = true;
    }
  }
}

function submitDelete() {
    var checkboxes = document.getElementsByName(checkboxName);
    var selectedCandidateIds = [];
    for (var i = 0; i < checkboxes.length; i++) {
        var checkbox = checkboxes[i];
        if (checkbox.checked) {
            selectedCandidateIds.push(checkbox.value);
        }
    }
    if (selectedCandidateIds.length > 0) {
        var deleteData = JSON.stringify(selectedCandidateIds);
        postRequest('/candidates', deleteData);
    }
}

function postRequest(url, data) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            window.location.reload();
        }
    };
    xhr.send(data);
}
