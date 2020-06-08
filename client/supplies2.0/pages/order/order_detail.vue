<template>
	<view>
		<cu-custom bgColor="bg-gradual-blue" :isBack="true">
			<block slot="content">订单详情</block>
		</cu-custom>
		
		<view class="cu-card card-margin" style="margin-bottom: -30upx;">
			<view class="cu-item">
				<view class="flex margin-left justify-between">
					<view class="flex text-left margin-top-sm text-gray" style="width: 100%;">
						{{order_detail_info.timeStr}}
					</view>
					<view class="cu-tag radius bg-light-blue">{{order_detail_info.order_status}}</view>
				</view>
				
				<view class="flex justify-between margin-left margin-right margin-top-sm">
					<view class="title margin-right">订单总额</view>
					<text class="text-right">{{order_detail_info.order_total_price}}</text>
				</view>
				
				<view class="flex justify-between margin-left margin-right margin-top-sm">
					<view class="title margin-right">归属部门</view>
					<text class="text-right">{{order_detail_info.order_apartment}}</text>
				</view>
				
				<view class="flex justify-between margin-left margin-right margin-top-sm margin-bottom">
					<view class="title margin-right">是否专项申请</view>
					<text class="text-right">{{order_detail_info.order_is_special ? '是' : '否'}}</text>
				</view>
				
			</view>
		</view>
		
		<view class="cu-card" v-for="(item, index) in order_detail_info.order_items" :key="index">
			<view class="cu-item" >
				<view class="flex">
					<view class="margin-top margin-left title">{{item.commodity_supplier}}</view>
					<view class="margin-top margin-left margin-right text-light-blue">{{item.commodity_status}}</view>
				</view>
				
				<view class=" cu-list menu-avatar" >
					<view class="cu-item padding-left" style="height: 200upx;">
						<view
							class="cu-avatar xl margin-left-sm"
							:style="
								item.commodity_image === null
									? 'background-image:url(../../static/default.png);'
									: 'background-image:url(' +
									  domain +
									  item.commodity_image +
									  ');'
							"
						></view>
						<view class="content4" style="width: calc(100% - 220upx);">
							<view class="flex justify-between">
								<view class="title">{{ item.commodity_name }}</view>
								<view class="title">￥{{item.commodity_total_price}} 元</view>
							</view>
							
							<view class="flex">
								<view class="text-grey text-df flex">
										规格:{{ item.commodity_specification }}
									</text>
								</view>
								<!-- <view class="text-grey text-df flex">
									<text class="text-cut margin-left-xs">
										| 型号:{{ item.asset_type }}
									</text>
								</view> -->
							</view>
				
							<view class="flex">
								<!-- <view class="text-grey text-df margin-right-sm">
									品牌: {{ item.asset_band }}
								</view> -->
								<view class="text-grey text-df">
									数量:{{item.commodity_count}}
								</view>
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
				order_detail_info:null
			}
		},
		onLoad(option) {
			console.log(option)
			if(option.orderDetailInfo !== undefined){
				let info = JSON.parse(decodeURIComponent(option.orderDetailInfo));
				this.order_detail_info = info;
				console.log('order detail');
				console.log(info);
			}
		},
		methods: {
			
		}
	}
</script>

<style>

</style>
