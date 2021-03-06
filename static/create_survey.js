var inps = [];
var instance = 154;

function refreshSpan() {
    if (inps.length == 1) {
        $(document).find("#num-questions").text("1 question");
    } else {
        $(document).find("#num-questions").text(inps.length + " questions");
    }
}

function removeQuestion(refBtn) {
    var num = $(refBtn).parent().find("#instance-id").text();
    for (let i = 0; i < inps.length; i ++) {
        if ($(inps[i]).find("#instance-id").text() == num) {
            inps.splice(i, 1);
            break;
        }
    }
    $(refBtn).parent().remove();
    refreshSpan();
}

function addMe(btn) {
    var other = $("<li></li>");
    var clone = $(btn).parent().find("div").clone();
    $(other).append(clone);
    var delButton = $("<button>", {type: "button", "class": "red"}).text("Remove this question");
    delButton.on("click", function() {
        removeQuestion(this);
    });
    var typeDropdown = $("<select>", {"class": "text-in"}).append($('<option>', {value: "choice", text: 'Multiple Choice'})).append($('<option>', {value: "text", text: 'Text Response'}));
    $(other).append(typeDropdown);
    $(other).append(delButton);
    //var mandatory = $("<input>", {type: "checkbox", name: "mandatory", "class": "checkbox", "checked": "true"});
    //$(clone).append(mandatory);
    //var txt = $("<span></span>").text("Mandatory");
    //$(clone).append(txt);
    var myId = $("<span></span>", {css: {"display": "none"}, id: "instance-id"}).text(instance + "");
    $(clone).append(myId);
    instance += 1;
    $(document.getElementById("question-container")).append(other);
    inps.push(other);
    refreshSpan();
}

function removeInput() {
    var container = $(document).find("#question-container");
    container.children().last().remove();
    inps.pop();
    refreshSpan();
}

function mySubmit() {
    if (inps.length < 1) {
        alert("You need at least 1 question for a valid survey.");
        return;
    }
    if (document.getElementById("title").value.length == 0) {
        alert("You need to have a proper title for the survey.");
        return;
    }
    var data = {"title": document.getElementById("title").value,
                "course": document.getElementById("offering").value,
                "questions": []};
    for (let i = 0; i < inps.length; ++i) {
        data["questions"].push({
            "id": Number($(inps[i]).find("span").first().text()),
            "type": $(inps[i]).find("select").val()
        });
    }

    document.getElementById("submission").disabled = true;

    var xhr = new XMLHttpRequest();
    var form = document.getElementById("main-form");

    xhr.open(form.method, form.action, true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

    xhr.send(JSON.stringify(data));

    window.setTimeout(function() {
        window.location.href='/create_survey/done';
    }, 500);

    // console.log(data);
}
