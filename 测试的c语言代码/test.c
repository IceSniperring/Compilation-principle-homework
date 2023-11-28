#include <iostream>
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <cstdlib>
#include <vector>
 
using namespace std;
 
int idtop=0;
 
struct file
{
    int id;
    string name;
    bool is_folder;
    int father;
}files[2001],*root=files;
 
vector<int>ct[2001];//content
 
int history[10005],htop=0,hcur=0;
int current;
 
string rem[2001];
string prefix(int depth)
{
    if(rem[depth]!="")  return rem[depth];
    string ret;
    for(int d = 1; d <= depth; d++)   ret+="..";
    return rem[depth]=ret;
}
 
void print(int id, int depth)
{
    //cout<<depth<<endl;
    cout<<prefix(depth)<<"\\"<<files[id].name<<endl;//   ../folder
    for(int i = 0; i < ct[id].size(); i++)
    {
        if(files[ct[id][i]].is_folder) print(ct[id][i],depth+1);
        else    cout<<prefix(depth+1)<<files[ct[id][i]].name<<endl;  
    }
}
 
int newFile(bool isf, string name)
{
    for(int i = 0; i < ct[current].size(); i++)
        if(files[ct[current][i]].name == name && files[ct[current][i]].is_folder == isf)  return -1;
    files[++idtop].id = idtop;
    files[idtop].name = name;
    files[idtop].father = current;
    files[idtop].is_folder = isf;
    ct[current].push_back(idtop);
    if(isf)
    {
        current = idtop;
        history[htop = ++hcur] = idtop;
    }
    return 1;
}
 
int enter(string path)
{
    int posi = 0, cur_bk = current;
    if(path[0]=='\\'||path[path.length()-1]!='\\')
    {
        return -1;
    }
    else
    {
        while(posi < path.length())
        {
            string split=""; int curlen = 0;
            while(posi<path.length())
            {
                char s = path[posi];
                if(path[posi]!='\\')    split+=path[posi],posi++,curlen++;
                else
                {
                    posi++;
                    if(curlen==0)   {current = cur_bk; return -1;}
                    bool found = false;
                    for(int i = 0; i < ct[current].size(); i++)  
                        if(files[ct[current][i]].name == split) 
                        {
                            if(files[ct[current][i]].is_folder == false)  continue;
                            found = true;
                            current = ct[current][i];
                            break;
                        }
                    if(!found)  {current = cur_bk; return -1;}
                    break;
                }
            }
            history[htop = ++hcur] = current;
        }
        return 1;
    }
}
 
int back()
{
    if(hcur)
    {
        current = history[--hcur];
        return 1;
    }else
    {
        return -1;
    }
}
 
int fore()
{
    if(hcur>=htop)
    {
        return -1;
    }else
    {
        current = history[++hcur];
        return 1;
    }
}
 
int up()
{
    if(files[current].father == -1)   return -1;
    else
    {
        current = files[current].father;
        history[htop = ++hcur] = current;
    }
}
 
void init()
{
    for(int i = 0; i < 35; i++)   rem[i]="";
    root->id = 0; root->name = "exp"; root->father = -1; root->is_folder = true;
    history[0] = 0;
    current = 0;
}
 
#define Wrong printf("%s\n","WRONG COMMAND.");
 
int main()
{
    //freopen("explorer.in","r",stdin);
    //freopen("explorer.out","w",stdout);
    init();
    int n;
    scanf("%d", &n);
    while(n--)
    {
        string com;
        cin>>com;
        if(com=="back")
        {
            if(back()==-1)  Wrong;
            continue;
        }
        if(com=="fore")
        {
            if(fore()==-1)  Wrong;
            continue;
        }
        if(com=="up")
        {
            if(up()==-1)    Wrong;
            continue;
        }
        if(com=="print")
        {
            print(0,0);
            continue;
        }
        if(com=="new")
        {
            getchar();
            char comd[51]; bool isf = false; string fname = "";
            gets(comd);
           for(int i = 0; i < strlen(comd); i++)
            {  
                if(comd[i]==' ') 
                {
                    isf = true;
                    continue;
                }
                if(isf)
                {
                    fname += comd[i];
                }
            }
            if(isf)
            {
                switch(comd[0])
                {
                    case '0':
                        if(comd[1]!=' ')
                        {
                            Wrong;
                            continue;
                        }
                        isf=false;
                        break;
                    case '1':
                        if(comd[1]!=' ')
                        {
                            Wrong;
                            continue;
                        }
                        break;
                    default:
                        Wrong;
                        continue;
                }
            }else
            {
                for(int i = 0; i < strlen(comd); i++)
                    fname += comd[i];
            }
            if(newFile(isf,fname)==-1)  Wrong;
            continue;
        }
        if(com=="enter")
        {
            string path;
            cin>>path;
            if(enter(path)==-1) Wrong;
            continue;
        }
    }
     
}