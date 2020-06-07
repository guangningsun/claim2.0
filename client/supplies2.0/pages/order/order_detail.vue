<template>
	<view>
		<cu-custom bgColor="bg-gradual-blue" :isBack="true">
			<block slot="content">订单详情</block>
		</cu-custom>
		
		<!-- <view class="cu-card card-margin" style="margin-bottom: -30upx;" v-for="(item,index) in install_device_list" :key="index"> -->
		<view class="cu-card card-margin" style="margin-bottom: -30upx;">
			<view class="cu-item">
				<view class="flex margin-left justify-between">
					<view class="flex text-left margin-top-sm text-gray" style="width: 100%;">
						ddd{{item.construction_createtime}}
					</view>
					<view class="cu-tag radius bg-light-blue">ddd{{item.deviceStatus}}</view>
				</view>
				
				<view class="flex justify-between margin-left margin-right margin-top-sm">
					<view class="title margin-right">订单总额</view>
					<text class="text-right">dd{{name}}</text>
				</view>
				
				<view class="flex justify-between margin-left margin-right margin-top-sm">
					<view class="title margin-right">归属部门</view>
					<text class="text-right">dd{{apart_name}}</text>
				</view>
				
				<view class="flex justify-between margin-left margin-right margin-top-sm margin-bottom">
					<view class="title margin-right">是否专项申请</view>
					<text class="text-right">dd{{apart_name}}</text>
				</view>
				
			</view>
		</view>
		
		<!-- <view class="cu-card" v-for="(item, index) in order_item_list" :key="index"> -->
		<view class="cu-card">
			<view class="cu-item" >
				<view class="margin-top margin-left text-light-blue">dd{{item.selected_supplier_name}}</view>
				<view class=" cu-list menu-avatar" >
					<view class="cu-item padding-left" style="height: 200upx;">
						<view
							class="cu-avatar xl margin-left-sm"
							:style="
								item.asset_image === null
									? 'background-image:url(../../static/default.png);'
									: 'background-image:url(' +
									  domain +
									  item.asset_image +
									  ');'
							"
						></view>
						<view class="content4" style="width: calc(100% - 220upx);">
							<view class="flex justify-between">
								<view class="title">ss{{ item.asset_name }}</view>
								<view class="title">￥ff{{item.total_price}}</view>
							</view>
							
							<view class="flex">
								<view class="text-grey text-df flex">
										规格:{{ item.asset_specification }}
									</text>
								</view>
								<view class="text-grey text-df flex">
									<text class="text-cut margin-left-xs">
										| 型号:{{ item.asset_type }}
									</text>
								</view>
							</view>
				
							<view class="flex">
								<view class="text-grey text-df margin-right-sm">
									品牌: {{ item.asset_band }}
								</view>
								<view class="text-grey text-df">
									| 数量:{{item.number}}
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
				
			}
		},
		onLoad(option) {
			console.log(option)
			if(option.orderDetailInfo !== undefined){
				let info = JSON.parse(decodeURIComponent(option.orderDetailInfo));
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
