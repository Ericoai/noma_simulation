#include<iostream>
#include <windows.h>
#include <stdio.h>
#include <windef.h>
#include<cstdio>
#include<cstring>
using namespace std;
const int maxn=110;
const int inf=0x7fffffff;
int n = 2,m = 2,w[maxn][maxn] = {{0,0,0},{0,100,1000},{0,15,34}};//n表示x边点的个数，y表示y边点的个数，w表示边权值
int lx[maxn],ly[maxn];//lx表示x边的标杆，ly表示y边的标杆
int from[maxn],to[maxn];//from[i]=j表示y边的i由x边的j连接。to[i]=j表示x边的i可以到达y边的j
bool s[maxn],t[maxn];//s表示x边的点集，t表示y边的点集
bool find(int x)//匈牙利算法
{
    s[x]=1;
    for(int i=1;i<=m;i++)
    if(lx[x]+ly[i]==w[x][i]&&!t[i])
    {
        t[i]=1;
        if(!from[i]||find(from[i]))
        {
            from[i]=x;
            to[x]=i;
            return 1;
        }
    }
    return 0;
}
void update()//更新标杆
{
    int d=inf;
    for(int i=1;i<=n;i++)
    if(s[i])
    for(int j=1;j<=m;j++)
    if(!t[j])
    d=min(d,lx[i]+ly[j]-w[i][j]);//按照上面给出的原则计算d
    for(i=1;i<=n;i++)//点集s中的点的标杆lx[i]-d
    if(s[i]) lx[i]-=d;
    for(int j=1;j<=m;j++)//点集t中的点的标杆ly[j]+d
    if(t[j]) ly[j]+=d;
}
void km()//km算法
{
    for(int i=1;i<=n;i++)//初始化标杆
      for(int j=1;j<=m;j++)
      lx[i]=max(lx[i],w[i][j]);
    for(i=1;i<=n;i++)//x边每个点的匹配
    for(;;)
    {
        memset(s,0,sizeof(s));
        memset(t,0,sizeof(t));
        if(find(i)) break;
        else update();
    }
}
int main()
{

    //scanf("%d %d",&n,&m);//输入
	int n = 2;
	int m = 2;
	/*
    for(int i=1;i<=n;i++)
      for(int j=1;j<=m;j++)
      scanf("%d",&w[i][j]);
	*/
	int w[3][3] = {{0,0,0},{0,100,1000},{0,15,34}};



    km();
    int ans=0;
    for(int i=1;i<=n;i++)//计算答案
	{
		ans+=w[i][to[i]];
		printf("%d\n",w[i][to[i]]);

	}
    printf("%d\n",ans);//输出
    return 0;
}
}
