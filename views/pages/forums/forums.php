<?php include('./views/layout/top.php'); ?>
<h2>Forums</h2>
<table class="forum-boards">
<? for ($j = 0; $j < 3; $j++): ?>
  <tr>
    <th colspan="5" class="category-header">Category Name</th>
  </tr>
  <tr>
    <td></td>
    <th>
      Forum
    </th>
    <th>
      Threads
    </th>
    <th>
      Posts
    </th>
    <th>
      Latest Post
    </th>
  </tr>
<? for ($i = 0; $i < 5; $i++): ?>
  <tr class="forum-board-row">
    <td class="forum-board-icon">
      <img src="/static/img/SHC.png">
    </td>
    <td class="forum-board-info">
      <a href="/forums/board">
        <span class="forum-board-link">Sample Board</span>
        <p>
          Sample board is the best place to talk about anything. You can make
          sample threads and keep on posting on other people's threads.
        </p>
      </a>
    </td>
    <td>
      5
    </td>
    <td>
      322
    </td>
    <td class="forum-latest-post">
      <a href="/forums/thread">Sample Thread is the world's longest
        thread title</a> by <a href="/user">User</a>
      on 5 May 2016 21:05 SST
    </td>
  </tr>
<? endfor; ?>
<? endfor; ?>
</table>
<?php include('./views/layout/bottom.php'); ?>
