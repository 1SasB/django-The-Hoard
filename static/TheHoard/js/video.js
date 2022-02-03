    // var myModal = document.getElementById('CommentModal')
    // var myInput = document.getElementById('getComment')

    // myModal.addEventListener('shown.bs.modal', function () {
    // myInput.focus()
    // })

console.log("Im in the video page javascript block")
          /* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myFunction(id) {
         console.log("im in my_function")
         x = document.getElementById("myDropdown");
         if (x.style.display === "none") {
           x.style.display = "block";
         } else {
           x.style.display = "none";
         }
       }

       
       function my_Function(id) {
         var x = document.getElementById("reply_container"+id);
         console.log("im in my_function")
         if (x.style.display === "none") {
           x.style.display = "block";
         } else {
           x.style.display = "none";
         }
       }

       function replyFunction(id) {
         console.log(id)
         var x = document.getElementById("reply_form"+id);
         console.log("im in replyfunction")
         if (x.style.display === "none") {
           x.style.display = "block";
         } else {
           x.style.display = "none";
         }
       }
    
       function SubscribeHord(url,hord_id){
           $.post(url, {}, function(rowz){
            console.log(url, 'finished')
            $("#unsubscribe_btn_"+hord_id).toggle();
            $("#subscribe_btn_"+hord_id).toggle();
           }).fail(function(xhr){
               alert('Url failed with '+xhr.status+' '+url)
           })
       }

       function unSubscribeHord(url,hord_id){
           $.post(url, {}, function(rowz){
            console.log(url, 'finished')
            $("#unsubscribe_btn_"+hord_id).toggle();
            $("#subscribe_btn_"+hord_id).toggle();
           }).fail(function(xhr){
               alert('Url failed with '+xhr.status+' '+url)
           })
       }
    
       function likeVid(url, video_id,chk) {
            console.log('Requesting JSON');
            $.post(url, {},  function(rowz){
                console.log(url, 'finished');
                $("#unlike_btn_"+video_id).toggle();
                $("#like_btn_"+video_id).toggle();
                if(chk=='1'){
                    $('#like_count').html(function(i, val) { return +val+1 });
                    // checking to see if dislike button is already on and switching it off
                    if($('#dislike_btn_'+video_id).is(':visible')){
                        $("#undislike_btn_"+video_id).toggle();
                        $("#dislike_btn_"+video_id).toggle();
                        $('#dislike_count').html(function(i, val) { return +val-1 });
                    }
                }else{
                    $('#like_count').html(function(i, val) { return +val-1 });
                }
            }).fail(function(xhr) {
                alert('Url failed with '+xhr.status+' '+url);
            });
        }

        function dislikeVid(url, video_id,chk) {
            console.log('Requesting JSON');
            $.post(url, {},  function(rowz){
                console.log(url, 'finished');
                $("#undislike_btn_"+video_id).toggle();
                $("#dislike_btn_"+video_id).toggle();
                if(chk=='1'){
                    $('#dislike_count').html(function(i, val) { return +val+1 });
                    // checking to see if like button is already on and switching it off
                    if($('#like_btn_'+video_id).is(':visible')){
                        $("#unlike_btn_"+video_id).toggle();
                        $("#like_btn_"+video_id).toggle();
                        $('#like_count').html(function(i, val) { return +val-1 });
                    }
                }else{
                    $('#dislike_count').html(function(i, val) { return +val-1 });
                }
            }).fail(function(xhr) {
                alert('Url failed with '+xhr.status+' '+url);
            });
        }

    
    //########################################################
    // COMENT AND REPLY FUNCTIONS BELOW
    
    function create_comment(){
        var commentInput = $('textarea[name="comment-text"]').val().trim();
        var video_id = $('input[name="video-id"]').val()
        console.log(video_id)
        if (commentInput) {
            // Create Ajax Call
            $.ajax({
                method: 'post',
                url: '/video/comment/create',
                data: {
                    'comment': commentInput,
                    'vid_id': video_id
                },
                dataType: 'json',
                success: function (data) {
                    if (data.comment) {
                        console.log(data.comment)
                    appendToCommentdiv(data.comment);
                    }
                }
            });
        } else {
            alert("All fields must be filled with a valid value.");
        }
        $('form#comment-form').trigger("reset");
        return false;
    }
    


function appendToCommentdiv(comment) {
  $("#comment-list").prepend(`
  <li class="comment-container${comment.id}" style="margin: 0px; padding: 0px;">
                                            <span style=" margin-bottom: 0px;" id="${comment.id}-comment-span">
                                                <p style="margin: 0px;" name="comment-user" >
                                                    ${comment.user}
                                                </p>
                                                    <!-- <a href="#" onclick="editComment({{comment.id}})" data-bs-toggle="modal" data-bs-target="#CommentModal" style="margin-right: 10px; margin-left: 10px;"><i class="bi bi-pencil"></i></a> -->
                                                    <a  href="#" id="getComment" data-bs-toggle="modal" data-bs-target="#commentModal" onclick="editComment(${comment.id})" ><i class="bi bi-pencil"></i></a>
                                                    <a  href="#" data-bs-toggle="modal" data-bs-target="#DeleteCommentModal" onclick="deleteComment(${comment.id})"><i class="bi bi-trash"></i></a>
                                                    <!-- <a href="#"><i class="bi bi-trash"></i></a> -->
                                                <p style="margin: 0px; font-size: 9px;" name="comment-date" >${comment.uploaded_date }</p>
                                                <p class="CommentText" style=" margin-bottom: 0px;" name="comment-text">
                                                    ${comment.comment_text}
                                                </p>
                                            </span>
                                            <div class="container" style="padding: 0px; margin-bottom: 7.5px; margin-top: 5px;">
                                                <!-- like button -->
                                                <span class="fa-stack" style="vertical-align: middle;">
                                                    <i class="far fa-thumbs-up fa-stack-1x" style="padding-left: 0px;"></i>
                                                    <i class="fas fa-thumbs-up fa-stack-1x"></i>
                            
                                                </span>
                                                <span class="fa-stack" style="vertical-align: middle; display: none;">
                                                    <i class="far fa-thumbs-up fa-stack-1x"></i>
                                                    <i class="fas fa-thumbs-up fa-stack-1x"></i>
                            
                                                </span>
                                                <span>2.5K</span>
                                                <!-- unlike button -->
            
                                                <span class="fa-stack" style="vertical-align: middle; display: none;">
                                                    <i class="far fa-thumbs-down fa-stack-1x"></i>
                                                    <i class="fas fa-thumbs-down fa-stack-1x"></i>
                                                </span>
                                                <span class="fa-stack" style="vertical-align: middle;">
                                                    <i class="far fa-thumbs-down fa-stack-1x"></i>
                                                    <i class="fas fa-thumbs-down fa-stack-1x"></i>
                                                </span>
                                                <span>2.5K</span>
                                                <a id="reply_btn" style="margin-left: 25px;" onclick="replyFunction(${comment.id})"><i class="bi bi-reply" style="font-size: 1.3rem; color: black;" ></i></a>
                                                <a onclick="my_Function(${comment.id})" style="margin-left: 20px;">
                                                    View replys
                                                </a> <!-- "onclick="my_Function()" href="#" style="margin-left: 20px;">View replys</a> -->
                                        
                                            </div>
                                            <div class="container" id="reply_form${comment.id}" style="display: none;">
                                                <form action="" id="reply-form" name="reply-form">
                                                    <input type="hidden" name="reply-comment-id" id="reply-comment-id${comment.id}" value="${comment.id}">
                                                    <input class="form-control form-control-sm" type="text" name="reply-comment-input" placeholder="Type a reply" id="reply-comment-input${comment.id}" >
                                                    <div style="margin-top: 8.5px;">
                                                        <button type="submit" class="btn btn-secondary btn-sm" id="reply_btn">Submit</button>
                                                        <button class="btn btn-secondary btn-sm" onclick="replyFunction(${comment.id})" >Cancel</button>
                                                    </div>
                                                </form>
                                                
                                                
                                            </div>

                                            <div id="reply-container${comment.id}">
                                            
                                                <div id="reply_container${comment.id}" style="display: none;">
                                                    
                                                    <ul class="list-unstyled" id="Reply_container${comment.id}" style="margin-left: 20px; margin-right: 4.5px;">
                                                        <li style="display: none;"></li>
                                                    </ul>
                                                    
                                                </div>
                                            
                                            </div>
                                            <hr>
                                        </li>
    `);
}


function editComment(id) {
  if (id) {
    sp_id = "#"+id+"-comment-span";
    console.log(sp_id)
    
    comment = $(sp_id).find(".CommentText").text().trim();
    console.log(id)
    console.log(comment)
    $('#edit-comment-reply-modal-title').html("EDIT COMMENT")
    $('#edit-modal-message-text').html("Comment:")
    $('#edit-comment-id').val(id);
    $('#edit-comment-text').text(comment);

  }
}

function deleteComment(id){
    if(id){
        sp_id = "#"+id+"-comment-span";
        console.log(sp_id)
    
        comment = $(sp_id).find(".CommentText").text().trim();
        console.log(comment)
        $('#delete-comment-reply-modal-title').text("DELETE COMMENT")
        $('#delete-modal-message-text').text("Comment:")
        $('#delete-comment-id').val(id);
        $('#delete-comment-text').text(comment);
    }
}

function update_comment(){

    var idInput = $('input[name="edit-comment-id"]').val();
    var commentInput = $('textarea[name="edit-comment-text"]').val().trim();
    console.log(commentInput)
    console.log(idInput)
    if (commentInput) {
        // Create Ajax Call
        $.ajax({
            method: 'post',
            url: '/video/comment/update',
            data: {
                'id': idInput,
                'comment': commentInput
            },
            dataType: 'json',
            success: function (data) {
                if (data.comment) {
                    updateToComment(data.comment);
                }
            }
        });
        } else {
        alert("All fields must have a valid value.");
    }
    $('form#update-Comment-form').trigger("reset");
    $('#commentModal').modal('hide');
    return false;

}

function delete_comment(){
    var idInput = $('input[name="delete-comment-id"]').val();
    console.log(idInput)
    if (idInput) {
        // Create Ajax Call
        $.ajax({
            method: 'post',
            url: '/video/comment/delete',
            data: {
                'id': idInput
            },
            dataType: 'json',
            success: function (data) {
                if (data.success_message) {
                    $(".comment-container"+data.comment_id).remove()
                    console.log(data.success_message)
                }
            }
        });
        } else {
        alert("All fields must have a valid value.");
    }
    $('form#delete-Comment-form').trigger("reset");
    $('#DeleteCommentModal').modal('hide');
    return false;

    
}






function updateToComment(comment){
    console.log("inside updateToComment function")
    $("#"+comment.id+"-comment-span").children("p").each(function() {
        var attr = $(this).attr("name");
        var attrs = $(this).text();
        console.log(attrs)
        if (attr == "comment-user") {
          $(this).text(comment.user);
        } else if (attr == "comment-date") {
          $(this).text(comment.updated_date);
        } else {
          $(this).text(comment.comment_text);
        }
      });
}

// Reply ajax fuunctions

$('form#reply-form').submit(function(){
    // var comment_id = $('input[name="reply-comment-id"]').val()
    var attr_id = $(this).children('input:first-child').val()
    console.log(attr_id)
    var comment_id = attr_id
    var reply_text = $("#reply-comment-input"+comment_id).val()
    console.log(reply_text)
    console.log(comment_id)
    if(reply_text){
        $.ajax({
            method: 'post',
            url: '/comment/reply/create',
            data: {
                'comment_id': comment_id,
                'reply': reply_text
            },
            dataType: 'json',
            success: function (data) {
                if (data.reply) {
                  console.log(data.reply.comment_id)
                  appendToReplydiv(data.reply);
                  
                }
            }
        });
    }else{
        alert("All fields must have a valid value")
    }
    $('form#reply-form').trigger("reset");
    return false;
})

// function ajxreply(){
    
// }

function appendToReplydiv(reply){
    $('#Reply_container'+reply.comment_id).append(`
    <li id="container_reply_${reply.comment_id}">
                                                                <div class="container" style="margin: 0px; padding: 0px;">
                                                                    <p style="margin: 0px;" name="reply-user">
                                                                        ${reply.user}
                                                                        <a  href="#" id="getComment" data-bs-toggle="modal" data-bs-target="#ReplyModal" onclick="editReply(${reply.id})" ><i class="bi bi-pencil"></i></a>
                                                                        <a  href="#" data-bs-toggle="modal" data-bs-target="#DeleteReplyModal" onclick="deleteReply(${reply.id})"><i class="bi bi-trash"></i></a>
                                                                    </p>
                                                                    <p style="margin: 0px; font-size: 9px;" name="reply-date">${reply.uploaded_date}</p>
                                                                </div>
                                                                <div class="container" id="${reply.id}-reply-container" style="margin: 0px; padding: 0px;">
                                
                                                                    <p class="ReplyText">
                                                                    ${reply.reply}
                                                                    </p>
                                                                    <div class="container" style=" margin-bottom: 7.5px; padding: 0px;">
                                                                        <!-- like button -->
                                                                        <span class="fa-stack" style="vertical-align: middle;">
                                                                            <i class="far fa-thumbs-up fa-stack-1x"></i>
                                                                            <i class="fas fa-thumbs-up fa-stack-1x"></i>
                                                    
                                                                        </span>
                                                                        <span class="fa-stack" style="vertical-align: middle; display: none;">
                                                                            <i class="far fa-thumbs-up fa-stack-1x"></i>
                                                                            <i class="fas fa-thumbs-up fa-stack-1x"></i>
                                                    
                                                                        </span>
                                                                        <span>2.5K</span>
                                                                        <!-- unlike button -->
                                
                                                                        <span class="fa-stack" style="vertical-align: middle; display: none;">
                                                                            <i class="far fa-thumbs-down fa-stack-1x"></i>
                                                                            <i class="fas fa-thumbs-down fa-stack-1x"></i>
                                                                        </span>
                                                                        <span class="fa-stack" style="vertical-align: middle;">
                                                                            <i class="far fa-thumbs-down fa-stack-1x"></i>
                                                                            <i class="fas fa-thumbs-down fa-stack-1x"></i>
                                                                        </span>
                                                                        <span>2.5K</span>
                                
                                
                                                                        <a href="#" id="reply_btn" style="margin-left: 25px;"><i class="bi bi-reply" style="font-size: 1.3rem; color: black;" ></i></a>
                                                                    </div>
                                                                    
                                                                </div>
                                                            </li>
    `)
}




function editReply(id) {
  if (id) {
    sp_id = "#"+id+"-reply-container";
    console.log(sp_id)
    
    reply = $(sp_id).find(".ReplyText").text().trim();
    console.log(id)
    console.log(reply)
    $('#edit-reply-modal-title').text("EDIT REPLY")
    $('#edit-reply-modal-message-text').text("Reply:")
    $('#edit-reply-id').val(id);
    $('#edit-reply-text').val(reply);

  }
}

function deleteReply(id){
    if(id){
        sp_id = "#"+id+"-reply-container";
        console.log(sp_id)
    
        reply = $(sp_id).find(".ReplyText").text().trim();
        console.log(reply)
        $('#delete-reply-modal-title').text("DELETE REPLY")
        $('#delete-reply-modal-message-text').text("Reply:")
        $('#delete-reply-id').val(id);
        $('#delete-reply-text').text(reply);
    }
}


function update_reply(){
    var idInput = $('input[name="edit-reply-id"]').val();
    var commentInput = $('textarea[name="edit-reply-text"]').val().trim();
    console.log(commentInput)
    console.log(idInput)
    if (commentInput) {
        // Create Ajax Call
        $.ajax({
            method: 'post',
            url: '/comment/reply/update',
            data: {
                'id': idInput,
                'reply': commentInput
            },
            dataType: 'json',
            success: function (data) {
                if (data.comment) {
                  updateToReply(data.comment);
                }
            }
        });
       } else {
        alert("All fields must have a valid value.");
    }
    $('form#update-Reply-form').trigger("reset");
    $('#ReplyModal').modal('toggle');
    console.log("finished updating reply >>>")
    // return false;
}


function updateToReply(reply){
    console.log("inside updateToComment function")
    $("#"+reply.id+"-reply-container").children("p").each(function() {
        var attr = $(this).attr("name");
        var attrs = $(this).text();
        console.log(attrs)
        if (attr == "reply-user") {
          $(this).text(reply.user);
        } else if (attr == "comment-date") {
          $(this).text(reply.updated_date);
        } else {
          $(this).text(reply.reply_text);
        }
      });
}

function delete_reply(){
    var idInput = $('input[name="delete-reply-id"]').val();
    console.log(idInput)
    if (idInput) {
        // Create Ajax Call
        $.ajax({
            method: 'post',
            url: '/comment/reply/delete',
            data: {
                'id': idInput
            },
            dataType: 'json',
            success: function (data) {
                if (data.success_message) {
                  $(".comment-container"+data.comment_id).remove()
                  console.log(data.success_message)
                }
            }
        });
       } else {
        alert("All fields must have a valid value.");
    }
    $('form#delete-Reply-form').trigger("reset");
    $('#DeleteReplyModal').modal('hide');
    return false;
}

