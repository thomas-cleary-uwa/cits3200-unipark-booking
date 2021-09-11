/* Functions to update selected booking on booking pages

Authors: Thomas Cleary,
*/

function turnCellOn(cell) {
  cell.classList.remove("timeslot-green");
  cell.classList.add("timeslot-yellow");
}


function turnCellOff(cell) {
  cell.classList.remove("timeslot-yellow");
  cell.classList.add("timeslot-green");
}


function isCellOn(cell) {
  return (cell.classList.contains("timeslot-yellow"));
}


function selectTimeslot(cellID) {
  let clickedCell = document.getElementById(cellID);

  // turn the cell on
  if (clickedCell.classList.contains("timeslot-green")) {
    // TURN OFF OTHER CELLS NOT IN THIS ROW
    updateTimetables(clickedCell);
  }
  // turn the cell off
  else {
    updateClickedRow(clickedCell);
  }

  updatePageBanner(clickedCell);
}


function updateTimetables(clickedCell) {
  let timetables = document.getElementsByClassName("timetable");
  let clickedRow = clickedCell.parentElement;

  for (let table of timetables) {
    let rows = table.getElementsByTagName("tr");

    for (let row of rows) {
      let cells = row.getElementsByTagName("td");

      // turn off cells not in the clicked row
      if (!(row == clickedRow)) {
        for (let cell of cells) {
          if (cell.classList.contains("timeslot-yellow")) {
            turnCellOff(cell);
          }
        }
      }

      // turn on cells in between previous selection and this clicked cell
      else {
        let turnOn = [];

        let foundClicked = false;
        let foundStart   = false;
        let logCells     = false;

        for (let cell of cells) {
          if (cell == clickedCell) {
            foundClicked = true;
            logCells = true;
            turnCellOn(cell); 
          }
          else if (!foundStart && cell.classList.contains("timeslot-yellow")) {
            foundStart = true;
            logCells = true;
          }

          if (logCells) {
            if (!isCellOn(cell)) {
              turnOn.push(cell);
            }
          }

          if (foundClicked && foundStart) {
            break;
          }
        }

        if (foundStart) {
          for (let cell of turnOn) {
            turnCellOn(cell);
          }
        }
      }
    }
  }
}

// turn of cells to left or right of clicked cell depending on which side has more
// turn off side with less
function updateClickedRow(clickedCell) {
  let clickedRow = clickedCell.parentElement;

  let leftOn =  [];
  let rightOn = [];
  let addLeft = true;

  let cells = clickedRow.getElementsByTagName("td");

  for (let cell of cells) {
    if (cell == clickedCell) {
      addLeft = false;
      continue;
    }
    else if (cell.classList.contains("timeslot-yellow")) {
      if (addLeft) {
        leftOn.push(cell);
      }
      else {
        rightOn.push(cell);
      }
    }
  }

  turnOffCells = [];
  if (leftOn.length < rightOn.length) {
    turnOffCells = leftOn;
  }
  else {
    turnOffCells = rightOn;
  }

  for (let cell of turnOffCells) {
    turnCellOff(cell);
  }
  turnCellOff(clickedCell);

}


function updatePageBanner(clickedCell) {
  let clickedRow = clickedCell.parentElement;

  let confirmBookingBtn = document.getElementById("confirm-button");
  let isTimeslotOn = checkTimeSlots()

  if (isTimeslotOn) {
    confirmBookingBtn.style.visibility = "visible";
  }
  else {
    confirmBookingBtn.style.visibility = "hidden";
  }
}


function checkTimeSlots() {
  let timetables = document.getElementsByClassName("timetable");

  for (let table of timetables) {
    for (let cell of table.getElementsByTagName("td")) {
      if (cell.classList.contains("timeslot-yellow")) {
        return true;
      }
    }
  }
  return false;
}