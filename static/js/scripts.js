function validateForm() {
    var x = document.forms["search_form"] ["title"].value;
    if (x == "") {
      alert("You gotta gimme something to search!");
      return false;
    }
  }