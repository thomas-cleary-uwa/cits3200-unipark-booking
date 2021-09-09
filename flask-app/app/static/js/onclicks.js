/* onclick functions for the app */

function confirmDelete(toDelete) {
  let msg = "Are you sure you want to delete " + toDelete + "?";
  return confirm(msg);
}


function selectTimeslot(cellID) {
  let clickedCell = document.getElementById(cellID);
  if (clickedCell.classList.contains("timeslot-green")) {
    checkTimetableCells(cellID);
    clickedCell.classList.remove("timeslot-green");
    clickedCell.classList.add("timeslot-yellow");
  }
  else {
    clickedCell.classList.remove("timeslot-yellow");
    clickedCell.classList.add("timeslot-green");
  }
}


function checkTimetableCells(clickedCellID) {
  let timetables = document.getElementsByClassName("timetable");
  let clickedCell = document.getElementById(clickedCellID);
  let activeRow = clickedCell.parentElement;
  
  for (let i = 0; i < timetables.length; i++) {
    let cells = timetables[i].getElementsByTagName("td");

    for (let j = 0; j < cells.length; j++) {
      let cell = cells[j];

      // if cell not in the row with the clicked cell
      // make it green
      if (cell.parentElement.id != activeRow.id) {
        if (cell.classList.contains("timeslot-yellow")) {
          cell.classList.remove("timeslot-yellow");
          cell.classList.add("timeslot-green");
        }
      }
    }
  }
  let clickedCellIdSplit = clickedCellID.split("-");
  let clickedCellSlot = clickedCellIdSplit[clickedCellIdSplit.length-1];
  console.log(clickedCellSlot);
}