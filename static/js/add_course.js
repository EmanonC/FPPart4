function  add() {
    var new_div = document.createElement("div");
    new_div.className = "autocomplete";

    var form = document.createElement("input");
    form.type = "text";
    form.name = "skillName";
    form.className = "form-control";
    form.placeholder = "Course Name";

    new_div.appendChild(form);
    var br = document.createElement("br");
    // new_div.appendChild(br)

    var element = document.getElementById("shit");
    element.appendChild(new_div);
    element.appendChild(br);

}