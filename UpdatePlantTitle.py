import ChangeWordpressPost

#action
client = ChangeWordpressPost.getclient()

for id in ChangeWordpressPost.plantDic:
    #获取文章
    post = ChangeWordpressPost.getWordpressPost(client,id)
    #更新标题
    post = ChangeWordpressPost.updatePlantAllContent(post)

    #更新文档并且输出log
    if(ChangeWordpressPost.EditPost(client,id,post)):
        print(id,"更新完成！")
    else:
        print(id,"更新失败！")