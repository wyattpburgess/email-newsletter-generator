$(document).ready(function () {
  $("#manage_newsletters").DataTable({
    columnDefs: [
      {
        targets: "no-sort",
        orderable: false,
      },
    ],
  });
  $("#manage_articles").DataTable({
    columnDefs: [
      {
        targets: "no-sort",
        orderable: false,
      },
    ],
  });
  $("#manage_categories").DataTable({
    columnDefs: [
      {
        targets: "no-sort",
        orderable: false,
      },
    ],
  });
});
