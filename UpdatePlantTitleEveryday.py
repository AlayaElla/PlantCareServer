import ChangeWordpressPost

#action
client = ChangeWordpressPost.getclient()

for id in ChangeWordpressPost.plantDic:
    print(id)

    #获取文章
    post = ChangeWordpressPost.getWordpressPost(client,id) 
    #更新标题
    post = ChangeWordpressPost.updatePlantTitle(post)

    #更新文档并且输出log
    if(ChangeWordpressPost.EditPost(client,entry["flower"],post)):
        print(id,"更新完成！")
    else:
        print(id,"更新失败！")