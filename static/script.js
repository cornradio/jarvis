// JARVIS DASHBOARD 外部核心脚本

window.executeCommand = function(t) {
    fetch('/command', { 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' }, 
        body: JSON.stringify({ text: t }) 
    }).then(function(res) {
        var ct = res.headers.get("content-type");
        // 获取后端通过 X-File-Name 传过来的原始文件名
        var rawFileName = res.headers.get("X-File-Name");
        
        // 如果是文件二进制流，则处理下载
        if (ct && ct.indexOf("json") === -1) {
            res.blob().then(function(blob) {
                var a = document.createElement('a');
                a.href = URL.createObjectURL(blob);
                // 优先使用后端传来的原名，否则根据类型兜底
                var filename = rawFileName || ("JARVIS_" + Date.now() + (ct.indexOf("image") !== -1 ? ".png" : ".dat"));
                a.download = filename;
                a.click();
            });
        }
        
        if (t.indexOf("切换") !== -1) {
            setTimeout(function() { location.reload(); }, 300);
        }
    });
};

window.doReload = function() {
    fetch('/reload', { method: 'POST' }).then(function() {
        location.reload();
    });
};

window.send = window.executeCommand;
