function validateForm() {
    var x = document.forms["searchForm"] ["name"].value;
    if (x == "") {
      alert("You gotta gimme something to search!");
      return false;
    }
  }