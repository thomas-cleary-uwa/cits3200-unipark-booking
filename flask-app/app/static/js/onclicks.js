/* onclick functions for the app

Authors: Thomas Cleary,
*/

function confirmDelete(toDelete) {
  let msg = "Are you sure you want to delete " + toDelete + "?";
  return confirm(msg);
}

// let clickedCellIdSplit = clickedCellID.split("-");
// let clickedCellSlot = clickedCellIdSplit[clickedCellIdSplit.length-1];
// console.log(clickedCellSlot);