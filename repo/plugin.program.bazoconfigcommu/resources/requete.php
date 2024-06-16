<?php
header('Content-Type: application/json');

$db = new SQLite3('vstream.db');  // Assurez-vous que le chemin est correct

$action = $_GET['action'] ?? null;

switch ($action) {
    case 'getBookmarks':
        $stmt = $db->prepare('SELECT * FROM favorite ORDER BY addon_id DESC');
        $result = $stmt->execute();
        $data = [];
        while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
            $data[] = $row;
        }
        echo json_encode($data);
        break;

    case 'insertBookmark':
        $data = json_decode(file_get_contents('php://input'), true);
        $stmt = $db->prepare('INSERT INTO favorite (title, siteurl, site, fav, cat, icon, fanart) VALUES (?, ?, ?, ?, ?, ?, ?)');
        $stmt->bindValue(1, $data['title']);
        $stmt->bindValue(2, $data['siteurl']);
        $stmt->bindValue(3, $data['site']);
        $stmt->bindValue(4, $data['fav']);
        $stmt->bindValue(5, $data['cat']);
        $stmt->bindValue(6, $data['icon']);
        $stmt->bindValue(7, $data['fanart']);
        try {
            $stmt->execute();
            echo json_encode(['success' => true]);
        } catch (Exception $e) {
            echo json_encode(['error' => $e->getMessage()]);
        }
        break;

    case 'delBookmark':
        $siteurl = $_GET['siteurl'] ?? null;
        $title = $_GET['title'] ?? null;
        $all = $_GET['all'] ?? null;
        $cat = $_GET['cat'] ?? null;

        if ($all) {
            $stmt = $db->prepare('DELETE FROM favorite');
        } elseif ($title && $siteurl) {
            $stmt = $db->prepare('DELETE FROM favorite WHERE siteurl = ? AND title = ?');
            $stmt->bindValue(1, $siteurl);
            $stmt->bindValue(2, $title);
        } elseif ($siteurl) {
            $stmt = $db->prepare('DELETE FROM favorite WHERE siteurl = ?');
            $stmt->bindValue(1, $siteurl);
        } elseif ($cat) {
            $stmt = $db->prepare('DELETE FROM favorite WHERE cat = ?');
            $stmt->bindValue(1, $cat);
        }

        if ($stmt) {
            try {
                $stmt->execute();
                echo json_encode(['success' => true]);
            } catch (Exception $e) {
                echo json_encode(['error' => $e->getMessage()]);
            }
        } else {
            echo json_encode(['error' => 'Invalid parameters']);
        }
        break;

    case 'getHistory':
        $stmt = $db->prepare('SELECT * FROM history ORDER BY addon_id DESC');
        $result = $stmt->execute();
        $data = [];
        while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
            $data[] = $row;
        }
        echo json_encode($data);
        break;

    case 'insertHistory':
        $data = json_decode(file_get_contents('php://input'), true);
        $stmt = $db->prepare('INSERT INTO history (title, disp, icone) VALUES (?, ?, ?)');
        $stmt->bindValue(1, $data['title']);
        $stmt->bindValue(2, $data['disp']);
        $stmt->bindValue(3, $data['icone']);
        try {
            $stmt->execute();
            echo json_encode(['success' => true]);
        } catch (Exception $e) {
            echo json_encode(['error' => $e->getMessage()]);
        }
        break;

    case 'delHistory':
        $searchtext = $_GET['searchtext'] ?? null;
        if ($searchtext) {
            $stmt = $db->prepare('DELETE FROM history WHERE title = ?');
            $stmt->bindValue(1, $searchtext);
        } else {
            $stmt = $db->prepare('DELETE FROM history');
        }

        if ($stmt) {
            try {
                $stmt->execute();
                echo json_encode(['success' => true]);
            } catch (Exception $e) {
                echo json_encode(['error' => $e->getMessage()]);
            }
        } else {
            echo json_encode(['error' => 'Invalid parameters']);
        }
        break;

    case 'insertWatched':
        $data = json_decode(file_get_contents('php://input'), true);
        $stmt = $db->prepare('INSERT INTO watched (tmdb_id, title_id, title, siteurl, site, cat, fav, season) VALUES (?, ?, ?, ?, ?, ?, ?, ?)');
        $stmt->bindValue(1, $data['tmdb_id']);
        $stmt->bindValue(2, $data['title_id']);
        $stmt->bindValue(3, $data['title']);
        $stmt->bindValue(4, $data['siteurl']);
        $stmt->bindValue(5, $data['site']);
        $stmt->bindValue(6, $data['cat']);
        $stmt->bindValue(7, $data['fav']);
        $stmt->bindValue(8, $data['season']);
        try {
            $stmt->execute();
            echo json_encode(['success' => true]);
        } catch (Exception $e) {
            echo json_encode(['error' => $e->getMessage()]);
        }
        break;

    case 'getWatched':
        $titleWatched = $_GET['titleWatched'];
        $stmt = $db->prepare('SELECT * FROM watched WHERE title_id = ?');
        $stmt->bindValue(1, $titleWatched);
        $result = $stmt->execute();
        $data = [];
        while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
            $data[] = $row;
        }
        echo json_encode($data);
        break;

    case 'getAllWatched':
        $stmt = $db->prepare('SELECT tmdb_id, * FROM watched ORDER BY addon_id DESC');
        $result = $stmt->execute();
        $data = [];
        while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
            $data[] = $row;
        }
        echo json_encode($data);
        break;

    case 'delWatched':
        $titleWatched = $_GET['titleWatched'];
        $stmt = $db->prepare('DELETE FROM watched WHERE title_id = ?');
        $stmt->bindValue(1, $titleWatched);
        try {
            $stmt->execute();
            echo json_encode(['success' => true]);
        } catch (Exception $e) {
            echo json_encode(['error' => $e->getMessage()]);
        }
        break;

    case 'insertResume':
        $data = json_decode(file_get_contents('php://input'), true);
        $stmt = $db->prepare('INSERT INTO resume (title, hoster, point, total) VALUES (?, ?, ?, ?)');
        $stmt->bindValue(1, $data['title']);
        $stmt->bindValue(2, $data['hoster']);
        $stmt->bindValue(3, $data['point']);
        $stmt->bindValue(4, $data['total']);
        try {
            $stmt->execute();
            echo json_encode(['success' => true]);
        } catch (Exception $e) {
            echo json_encode(['error' => $e->getMessage()]);
        }
        break;

    case 'getResume':
        $titleWatched = $_GET['titleWatched'];
        $stmt = $db->prepare('SELECT point, total FROM resume WHERE title = ?');
        $stmt->bindValue(1, $titleWatched);
        $result = $stmt->execute();
        $row = $result->fetchArray(SQLITE3_ASSOC);
        if ($row) {
            echo json_encode($row);
        } else {
            echo json_encode(['point' => 0, 'total' => 0]);
        }
        break;

    case 'delResume':
        $titleWatched = $_GET['titleWatched'];
        $stmt = $db->prepare('DELETE FROM resume WHERE title = ?');
        $stmt->bindValue(1, $titleWatched);
        try {
            $stmt->execute();
            echo json_encode(['success' => true]);
        } catch (Exception $e) {
            echo json_encode(['error' => $e->getMessage()]);
        }
        break;

    case 'insertViewing':
        $data = json_decode(file_get_contents('php://input'), true);
        $stmt = $db->prepare('INSERT INTO viewing (tmdb_id, title_id, title, siteurl, site, fav, cat, season) VALUES (?, ?, ?, ?, ?, ?, ?, ?)');
        $stmt->bindValue(1, $data['tmdb_id']);
        $stmt->bindValue(2, $data['title_id']);
        $stmt->bindValue(3, $data['title']);
        $stmt->bindValue(4, $data['siteurl']);
        $stmt->bindValue(5, $data['site']);
        $stmt->bindValue(6, $data['fav']);
        $stmt->bindValue(7, $data['cat']);
        $stmt->bindValue(8, $data['season']);
        try {
            $stmt->execute();
            echo json_encode(['success' => true]);
        } catch (Exception $e) {
            echo json_encode(['error' => $e->getMessage()]);
        }
        break;

    case 'getViewing':
        $stmt = $db->prepare('SELECT * FROM viewing GROUP BY title ORDER BY addon_id DESC');
        $result = $stmt->execute();
        $data = [];
        while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
            $data[] = $row;
        }
        echo json_encode($data);
        break;

    case 'delViewing':
        $titleWatched = $_GET['titleWatched'] ?? null;
        $cat = $_GET['cat'] ?? null;
        if ($titleWatched && $cat) {
            $stmt = $db->prepare('DELETE FROM viewing WHERE title_id = ? AND cat = ?');
            $stmt->bindValue(1, $titleWatched);
            $stmt->bindValue(2, $cat);
        } elseif ($titleWatched) {
            $stmt = $db->prepare('DELETE FROM viewing WHERE title_id = ?');
            $stmt->bindValue(1, $titleWatched);
        } elseif ($cat) {
            $stmt = $db->prepare('DELETE FROM viewing WHERE cat = ?');
            $stmt->bindValue(1, $cat);
        } else {
            $stmt = $db->prepare('DELETE FROM viewing');
        }

        if ($stmt) {
            try {
                $stmt->execute();
                echo json_encode(['success' => true]);
            } catch (Exception $e) {
                echo json_encode(['error' => $e->getMessage()]);
            }
        } else {
            echo json_encode(['error' => 'Invalid parameters']);
        }
        break;

    case 'insertDownload':
        $data = json_decode(file_get_contents('php://input'), true);
        $stmt = $db->prepare('INSERT INTO download (title, url, path, cat, icon, size, totalsize, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)');
        $stmt->bindValue(1, $data['title']);
        $stmt->bindValue(2, $data['url']);
        $stmt->bindValue(3, $data['path']);
        $stmt->bindValue(4, $data['cat']);
        $stmt->bindValue(5, $data['icon']);
        $stmt->bindValue(6, $data['size']);
        $stmt->bindValue(7, $data['totalsize']);
        $stmt->bindValue(8, $data['status']);
        try {
            $stmt->execute();
            echo json_encode(['success' => true]);
        } catch (Exception $e) {
            echo json_encode(['error' => $e->getMessage()]);
        }
        break;

    case 'getDownload':
        $url = $_GET['url'] ?? null;
        if ($url) {
            $stmt = $db->prepare('SELECT * FROM download WHERE url = ? AND status = 0');
            $stmt->bindValue(1, $url);
        } else {
            $stmt = $db->prepare('SELECT * FROM download');
        }
        $result = $stmt->execute();
        $data = [];
        while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
            $data[] = $row;
        }
        echo json_encode($data);
        break;

    case 'cleanDownload':
        $stmt = $db->prepare('DELETE FROM download WHERE status = 2');
        try {
            $stmt->execute();
            echo json_encode(['success' => true]);
        } catch (Exception $e) {
            echo json_encode(['error' => $e->getMessage()]);
        }
        break;

    case 'resetDownload':
        $url = $_GET['url'];
        $stmt = $db->prepare('UPDATE download SET status = 0 WHERE status = 2 AND url = ?');
        $stmt->bindValue(1, $url);
        try {
            $stmt->execute();
            echo json_encode(['success' => true]);
        } catch (Exception $e) {
            echo json_encode(['error' => $e->getMessage()]);
        }
        break;

    case 'delDownload':
        $url = $_GET['url'] ?? null;
        $path = $_GET['path'] ?? null;
        if ($url) {
            $stmt = $db->prepare('DELETE FROM download WHERE url = ?');
            $stmt->bindValue(1, $url);
        } elseif ($path) {
            $stmt = $db->prepare('DELETE FROM download WHERE path = ?');
            $stmt->bindValue(1, $path);
        }

        if ($stmt) {
            try {
                $stmt->execute();
                echo json_encode(['success' => true]);
            } catch (Exception $e) {
                echo json_encode(['error' => $e->getMessage()]);
            }
        } else {
            echo json_encode(['error' => 'Invalid parameters']);
        }
        break;

    case 'cancelDownload':
        $stmt = $db->prepare('UPDATE download SET status = 0 WHERE status = 1');
        try {
            $stmt->execute();
            echo json_encode(['success' => true]);
        } catch (Exception $e) {
            echo json_encode(['error' => $e->getMessage()]);
        }
        break;

    case 'updateDownload':
        $data = json_decode(file_get_contents('php://input'), true);
        $stmt = $db->prepare('UPDATE download SET size = ?, totalsize = ?, status = ? WHERE path = ?');
        $stmt->bindValue(1, $data['size']);
        $stmt->bindValue(2, $data['totalsize']);
        $stmt->bindValue(3, $data['status']);
        $stmt->bindValue(4, $data['path']);
        try {
            $stmt->execute();
            echo json_encode(['success' => true]);
        } catch (Exception $e) {
            echo json_encode(['error' => $e->getMessage()]);
        }
        break;

    default:
        echo json_encode(['error' => 'Invalid action']);
        break;
}

$db = null;
?>
