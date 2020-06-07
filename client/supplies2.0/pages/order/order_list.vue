<template>
	<view>
		<cu-custom bgColor="bg-gradual-blue" :isBack="false">
			<block slot="content">历史订单</block>
		</cu-custom>

<!-- 		<view class="cu-bar bg-white search fixed" :style="[{top:CustomBar + 'px'}]">
			<view class="search-form round">
				<text class="cuIcon-search"></text>
				<input class="padding-right-xl" type="text" placeholder="搜索物品" confirm-type="search" v-model="search_item" @input="onInput"></input>
				<view >
					<button class="cu-btn round bg-light-blue" @tap="onSearch">搜索</button>
				</view>
			</view>
		</view> -->

		<view v-show="showEmpty" style="margin-top: 200upx;">
			<view class="flex justify-center align-center margin-left-xl">
				<image src="../../static/empty_icon.png" style="width: 200upx; height: 200upx;" />
			</view>
			<view class="flex justify-center text-gray margin-top">空空如也</view>
		</view>
		
		<view class="cu-card" v-for="(item, index) in order_list" :key="index" @tap="goToDetail(item)">
			<view class="cu-item" style="margin-bottom: -10upx;">
				<view class="flex justify-between">
					<view class="margin-top margin-left title text-bold">{{item.order_apartment_name}}</view>
					<view class="margin-top margin-right title text-gray">状态{{item.order_status}}</view>
				</view>
				<view class=" cu-list menu-avatar" >
					<view class="cu-item padding-left" style="height: 200upx;">
						<view
							class="cu-avatar xl margin-left-sm"
							:style="
								item.order_image === null
									? 'background-image:url(../../static/default.png);'
									: 'background-image:url(' +
									  domain +
									  item.order_image +
									  ');'
							"
						></view>
						<view class="content4" style="width: calc(100% - 220upx);">
							<view class="flex justify-between">
								<view class="title text-lg text-orange">￥{{item.order_total_price}}</view>
								<view class="title text-gray">共{{ item.order_items.length }}件</view>
							</view>
							
							<view class="text-grey ">
									{{ item.order_create_time }}
								</text>
							</view>
							
						</view>
					</view>
				</view>
			</view>
		</view>

	</view>
</template>

<script>

export default {
	data() {
		return {

			showEmpty: false,
			
			order_list:[]
		};
	},
	onLoad() {
		uni.showLoading({
			title: '加载中...',
			mask: true
		});
	},
	onShow() {
		this.loadData();
	},
	methods: {

		successCb(rsp) {
			console.log(rsp.data);
			if (rsp.data.error === 0) {
				this.order_list = rsp.data.msg.order_info;
				
				if (this.order_list.length == 0) {
					this.showEmpty = true;
					return;
				}
				
				// console.log('commoditycategory:');
				// console.log(this.catList);
				// getApp().globalData.catList = this.cartList;

				// if (this.catList.length > 0) {
				// 	this.showNoMore = true;
				// }

				if (this.order_list.length == 0) {
					this.showEmpty = true;
					return;
				}

				
			}
			uni.hideLoading();
		},
		failCb(err) {
			uni.hideLoading();
			console.log('get_all_order_list failed', err);
		},
		completeCb(rsp) {},

		loadData() {
			
			this.requestWithMethod(
				getApp().globalData.get_all_order_info_list + uni.getStorageSync(getApp().globalData.key_wx_openid),
				'GET',
				'',
				this.successCb,
				this.failCb,
				this.completeCb
			);
		},

		goToDetail(item){
			console.log(item);
			uni.navigateTo({
				url: 'order_detail?orderDetailInfo=' + encodeURIComponent(JSON.stringify(item))
			})
		}
	}
};
</script>

<style>
.fixed {
	position: fixed;
	z-index: 99;
}

.VerticalNav.nav {
	width: 200upx;
	white-space: initial;
}

.VerticalNav.nav .cu-item {
	width: 100%;
	text-align: center;
	background-color: #fff;
	margin: 0;
	border: none;
	height: 50px;
	position: relative;
}

.VerticalNav.nav .cu-item.cur {
	background-color: #f1f1f1;
}

.VerticalNav.nav .cu-item.cur::after {
	content: '';
	width: 8upx;
	height: 30upx;
	border-radius: 10upx 0 0 10upx;
	position: absolute;
	background-color: currentColor;
	top: 0;
	right: 0upx;
	bottom: 0;
	margin: auto;
}

.VerticalBox {
	display: flex;
}

.VerticalMain {
	background-color: #f1f1f1;
	flex: 1;
}
</style>
