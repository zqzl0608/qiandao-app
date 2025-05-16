// Auto.js脚本
let accounts = ['zl1110','zl1111','zl1112','zl1113','zl1114','zl1115','zl1116','zl1117','zl1118','zl1119'];

// 主函数
function main() {
    // 打开网页
    app.startActivity({
        action: "android.intent.action.VIEW",
        data: "https://sgs.zce8.com/index/cdk"
    });
    
    // 等待页面加载
    sleep(3000);
    
    // 选择服务器
    click("服务器");
    sleep(1000);
    click("3");
    
    // 输入CDK
    setText("sgs2025");
    
    // 循环处理每个账号
    for (let account of accounts) {
        // 输入账号
        setText(account);
        sleep(1000);
        
        // 点击获取角色列表
        click("获取角色列表");
        sleep(5000);
        
        // 选择角色
        click("角色列表");
        sleep(1000);
        click("角色1");
        sleep(5000);
        
        // 处理验证码
        handleCaptcha();
        
        // 点击领取
        click("领取");
        sleep(5000);
        
        // 处理结果
        handleResult();
    }
}

// 处理验证码
function handleCaptcha() {
    // 点击验证码图片
    click("验证码");
    sleep(3000);
    
    // 这里需要OCR识别验证码
    // 可以使用Auto.js的OCR插件或其他方式
    
    // 输入验证码
    setText("验证码结果");
    sleep(1000);
}

// 处理领取结果
function handleResult() {
    let result = text("领取成功！").exists() ? "领取成功！" : 
                 text("领取次数已达上限").exists() ? "领取次数已达上限" : "验证码错误";
    
    console.log(result);
    
    // 点击确定按钮
    click("确定");
    sleep(1000);
    
    // 如果验证码错误，重试
    if (result == "验证码错误") {
        handleCaptcha();
    }
}

// 运行主函数
main(); 