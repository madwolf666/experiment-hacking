import pyxhook

def OnKeyPress(event):
    print(event)

#HookManagerクラスのインスタンス生成
new_hook = pyxhook.HookManager()
#キーストロークを待ち受ける
new_hook.KeyDown = OnKeyPress
#キーボードをフックする
new_hook.HookKeyboard()
#キーボードロギングセッションを開始する
new_hook.start()
