$(document).ready(function () {
  // --- Photo preview function ---
  function previewPhotoInput(input, preview) {
    const chosenFile = input[0].files[0];
    if (chosenFile) {
      const reader = new FileReader();
      reader.addEventListener('load', function () {
        preview.attr('src', reader.result);
      });
      reader.readAsDataURL(chosenFile);
    }
  }

  $("#formFile").change(function () {
    previewPhotoInput($("#formFile"), $("#photo-preview"));
  });

  $("#editFormFile").change(function () {
    previewPhotoInput($("#editFormFile"), $("#edit_photo_preview"));
  });

  // --- Add student form submission ---
  $("#addStudentForm").on("submit", function (event) {
    event.preventDefault();

        // ✅ INSERT FORMAT CHECK HERE
    const studentId = $("input[name='student_id']").val();
    const idPattern = /^\d{4}-\d{4}$/;
    if (!idPattern.test(studentId)) {
      $("#erroraddstdmsg").text("Invalid ID format. Use xxxx-xxxx").show();
      return; // stop submission
    }

    const preview2 = $('#photo-preview');

    $('body').append(`
      <div class="loading-overlay">
        <div class="spinner-border me-3" style="width: 3rem; height: 3rem;">
          <span class="visually-hidden">Loading...</span>
        </div>
        <h2>Adding Student<br>This should only take a minute...</h2>
      </div>
    `);

    $.ajax({
      type: "POST",
      url: "/student/add",
      data: new FormData(this),
      contentType: false,
      processData: false,
    }).done(function (data) {
      $('.loading-overlay').remove();

      if (data.error) {
        $("#erroraddstdmsg").text(data.error).show();
        preview2.attr('src', urlimg); // fallback image
      } else {
        alert("Successfully added student");
        window.location.href = "/student";
      }
    });
  });

  // --- Delete Student Modal setup ---
  $('#deleteStudent').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var studentId = button.data('student-id');
    var modal = $(this);

    if (!studentId) {
      modal.find('#errordeletstdemsg')
        .text("Error: Student ID not found on button. Please check the template.")
        .show();
      modal.find('#deleteStudentId').val('');
      modal.find('#studentIdDisplay').text('');
      return;
    }

    modal.find('#deleteStudentId').val(studentId);
    modal.find('#studentIdDisplay').text(studentId);
    modal.find('#errordeletstdemsg').hide();
  });

  // Handle delete form submission via AJAX
$('#deleteStudent').on('show.bs.modal', function (event) {
    const button = $(event.relatedTarget); // The button that triggered the modal
    const studentId = button.data('student-id');
    const modal = $(this);

    if (!studentId) {
      modal.find('#errordeletstdemsg')
        .text("Error: Student ID not found on button. Please check the template.")
        .show();
      modal.find('#deleteStudentId').val('');
      modal.find('#studentIdDisplay').text('');
      return;
    }

    // Set the hidden field and display ID in modal
    modal.find('#deleteStudentId').val(studentId);
    modal.find('#studentIdDisplay').text(studentId);
    modal.find('#errordeletstdemsg').hide();
  });

  // Handle delete form submission via AJAX
  $("#deleteStudentForm").on("submit", function (event) {
    event.preventDefault();

    const studentId = $("#deleteStudentId").val();
    const $errorMsg = $("#errordeletstdemsg");

    if (!studentId) {
      $errorMsg.text("Missing student ID.").show();
      return;
    }

    // Show loading overlay
    $('body').append(`
      <div class="loading-overlay">
        <div class="spinner-border me-3" style="width: 3rem; height: 3rem;">
          <span class="visually-hidden">Loading...</span>
        </div>
        <h2>Deleting Student<br>This should only take a minute...</h2>
      </div>
    `);

    $.ajax({
      type: "POST",
      url: "/student/delete",
      data: { student_id: studentId },
      dataType: "json"
    })
    .done(function (data) {
      $('.loading-overlay').remove();
      $("#deleteStudent").modal("hide");

      if (data.error) {
        $errorMsg.text(data.error).show();
      } else if (data.success) {
        // Show success message
        $("#successdeletstdemsg")
          .text("✅ Successfully deleted student with ID: " + studentId)
          .show();

        // Optional: hide after a delay then refresh
        setTimeout(function () {
          window.location.href = "/student";
        }, 3000);
      } else {
        $errorMsg.text("Unexpected response from server.").show();
      }
    })

    .fail(function (xhr, textStatus, errorThrown) {
      $('.loading-overlay').remove();
      $("#deleteStudent").modal("hide");
      $errorMsg.text("Error deleting student: " + textStatus).show();
      console.error("AJAX error:", textStatus, errorThrown);
    });
  });


  // --- Edit Student ---
  $(".edit-Student").on("click", function () {
    
    var id = $(this).data("student-id");
    var firstname = $(this).data("student-firstname");
    var lastname = $(this).data("student-lastname");
    var course_code = $(this).data("student-course");
    var year = $(this).data("student-year");
    var gender = $(this).data("student-gender");
    var picture = $(this).data("student-picture");
    
    

    const preview = $('#edit_photo_preview');
    if (picture !== 'None') {
      preview.attr('src', picture);
    } else {
      preview.attr('src', urlimg); // fallback image URL you define somewhere
    }

    $("#edit_student_id").val(id);
    $("#edit_student_first_name").val(firstname);
    $("#edit_student_last_name").val(lastname);
    $("#edit_student_course_code").val(course_code);
    $("#edit_student_year").val(year);
    $("#edit_student_gender").val(gender);

    $("#editStudentForm").off("submit").on("submit", function (event) {
      event.preventDefault();
      // Inside the edit form submit handler, add this at the top:
      const editStudentId = $("#edit_student_id").val();
      const idPattern = /^\d{4}-\d{4}$/;
      if (!idPattern.test(editStudentId)) {
        $("#erroreditstdmsg").text("Invalid ID format. Use xxxx-xxxx").show();
        return; // stop submission
}
      var formData = new FormData(this);
      formData.append('pastid', id);

      $('body').append(`
        <div class="loading-overlay">
          <div class="spinner-border me-3" style="width: 3rem; height: 3rem;">
            <span class="visually-hidden">Loading...</span>
          </div>
          <h2>Editing Student<br>This should only take a minute...</h2>
        </div>
      `);

      $.ajax({
        type: "POST",
        url: "/student/edit",
        data: formData,
        contentType: false,
        processData: false,
      }).done(function (data) {
        $('.loading-overlay').remove();

        if (data.error) {
          $("#erroreditstdmsg").text(data.error).show();
          preview.attr('src', urlimg);
        } else {
          alert("Successfully edited student");
          window.location.href = "/student";
        }
      });
    });
  });

  // --- Go back button ---
  $("#gobackstudent").on("click", function () {
    window.location.href = "/student";
  });
});
