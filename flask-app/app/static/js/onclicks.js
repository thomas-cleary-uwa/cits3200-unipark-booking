/* onclick functions for the app */

function confirmDelete(toDelete) {
  let msg = "Are you sure you want to delete " + toDelete + "?";
  return confirm(msg);
}


function selectTimeslot(cellID) {
  console.log(cellID);
  clickedCell = document.getElementById(cellID);
  if (clickedCell.classList.contains("timeslot-green")) {
    clickedCell.classList.remove("timeslot-green");
    clickedCell.classList.add("timeslot-yellow");
  }
  else {
    clickedCell.classList.remove("timeslot-yellow");
    clickedCell.classList.add("timeslot-green");
  }
}
