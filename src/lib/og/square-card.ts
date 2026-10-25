import satori from "satori";
import sharp from "sharp";
import { loadFonts } from "./og-card";

export const SQUARE_SIZE = 1080;

export type SquareCardData = {
	siteTitle: string;
	title: string;
	excerpt?: string | null;
	priceText?: string;
	category?: string;
	domain?: string;
};

type Node = { type: string; props: { style?: Record<string, unknown>; children?: unknown } };

function titleSizeFor(len: number): number {
	if (len <= 25) return 60;
	if (len <= 45) return 50;
	if (len <= 70) return 42;
	return 36;
}

export function buildSquareCard(data: SquareCardData): Node {
	const title = data.title.trim();
	const titleSize = titleSizeFor(title.length);
	const brand = (data.siteTitle || "Kotabook").toUpperCase();
	const price = data.priceText || "Mulai Rp 14.000 / eks";
	const category = (data.category || "Jasa Cetak Buku").toUpperCase();

	return {
		type: "div",
		props: {
			style: {
				width: `${SQUARE_SIZE}px`,
				height: `${SQUARE_SIZE}px`,
				display: "flex",
				flexDirection: "column",
				justifyContent: "space-between",
				backgroundColor: "#0B0F19",
				padding: "54px 64px 48px 64px",
				fontFamily: "Inter",
				color: "#F8FAFC",
				boxSizing: "border-box",
			},
			children: [
				// 1. TOP HEADER BAR
				{
					type: "div",
					props: {
						style: {
							display: "flex",
							justifyContent: "space-between",
							alignItems: "center",
							width: "100%",
							borderBottom: "1px solid #1E293B",
							paddingBottom: "24px",
						},
						children: [
							{
								type: "div",
								props: {
									style: {
										display: "flex",
										alignItems: "center",
										gap: "12px",
									},
									children: [
										{
											type: "div",
											props: {
												style: {
													width: "14px",
													height: "14px",
													borderRadius: "9999px",
													backgroundColor: "#10B981",
												},
											},
										},
										{
											type: "span",
											props: {
												style: {
													fontFamily: "JetBrains Mono",
													fontSize: "22px",
													fontWeight: 700,
													letterSpacing: "0.08em",
													color: "#F8FAFC",
												},
												children: brand,
											},
										},
										{
											type: "span",
											props: {
												style: {
													fontSize: "16px",
													color: "#64748B",
													marginLeft: "8px",
												},
												children: "• STANDAR PENERBIT",
											},
										},
									],
								},
							},
							{
								type: "div",
								props: {
									style: {
										backgroundColor: "rgba(245, 158, 11, 0.15)",
										border: "1px solid rgba(245, 158, 11, 0.4)",
										borderRadius: "9999px",
										padding: "8px 20px",
										display: "flex",
										alignItems: "center",
										gap: "8px",
									},
									children: [
										{
											type: "span",
											props: {
												style: {
													fontFamily: "JetBrains Mono",
													fontSize: "15px",
													fontWeight: 700,
													color: "#FBBF24",
													letterSpacing: "0.05em",
												},
												children: "100% GARANSI RETUR",
											},
										},
									],
								},
							},
						],
					},
				},

				// 2. MAIN TITLE SECTION
				{
					type: "div",
					props: {
						style: {
							display: "flex",
							flexDirection: "column",
							gap: "12px",
							marginTop: "16px",
							marginBottom: "16px",
						},
						children: [
							{
								type: "span",
								props: {
									style: {
										fontFamily: "JetBrains Mono",
										fontSize: "16px",
										fontWeight: 700,
										letterSpacing: "0.1em",
										color: "#38BDF8",
									},
									children: category,
								},
							},
							{
								type: "h1",
								props: {
									style: {
										fontSize: `${titleSize}px`,
										fontWeight: 700,
										lineHeight: 1.15,
										color: "#FFFFFF",
										margin: 0,
										padding: 0,
									},
									children: title,
								},
							},
							data.excerpt
								? {
										type: "p",
										props: {
											style: {
												fontSize: "22px",
												lineHeight: 1.4,
												color: "#94A3B8",
												margin: "8px 0 0 0",
											},
											children: data.excerpt,
										},
								  }
								: null,
						].filter(Boolean),
					},
				},

				// 3. PHYSICAL 3D BOOK & BADGE VISUAL
				{
					type: "div",
					props: {
						style: {
							display: "flex",
							justifyContent: "center",
							alignItems: "center",
							position: "relative",
							height: "400px",
							width: "100%",
							backgroundColor: "rgba(30, 41, 59, 0.4)",
							border: "1px solid #1E293B",
							borderRadius: "24px",
							padding: "20px",
						},
						children: [
							// 3D Book Graphic Container
							{
								type: "div",
								props: {
									style: {
										display: "flex",
										alignItems: "center",
										position: "relative",
										boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.8)",
									},
									children: [
										// Book Spine
										{
											type: "div",
											props: {
												style: {
													width: "36px",
													height: "320px",
													backgroundColor: "#1E1B4B",
													borderTopLeftRadius: "6px",
													borderBottomLeftRadius: "6px",
													borderRight: "2px solid #312E81",
													display: "flex",
													justifyContent: "center",
													alignItems: "center",
													color: "#FBBF24",
													fontSize: "14px",
													fontFamily: "JetBrains Mono",
												},
											},
										},
										// Book Front Cover
										{
											type: "div",
											props: {
												style: {
													width: "240px",
													height: "320px",
													backgroundColor: "#2E1065",
													borderTopRightRadius: "8px",
													borderBottomRightRadius: "8px",
													border: "1px solid #4C1D95",
													display: "flex",
													flexDirection: "column",
													justifyContent: "space-between",
													padding: "24px 20px",
													boxSizing: "border-box",
												},
												children: [
													{
														type: "div",
														props: {
															style: {
																display: "flex",
																flexDirection: "column",
																gap: "6px",
															},
															children: [
																{
																	type: "span",
																	props: {
																		style: {
																			fontSize: "12px",
																			fontFamily: "JetBrains Mono",
																			color: "#FBBF24",
																			letterSpacing: "0.1em",
																		},
																		children: "EDISI SPESIAL",
																	},
																},
																{
																	type: "span",
																	props: {
																		style: {
																			fontSize: "18px",
																			fontWeight: 700,
																			color: "#FFFFFF",
																			lineHeight: 1.2,
																		},
																		children: title.length > 40 ? title.slice(0, 38) + "…" : title,
																	},
																},
															],
														},
													},
													{
														type: "div",
														props: {
															style: {
																display: "flex",
																justifyContent: "space-between",
																alignItems: "center",
																borderTop: "1px solid #4C1D95",
																paddingTop: "12px",
															},
															children: [
																{
																	type: "span",
																	props: {
																		style: {
																			fontSize: "12px",
																			color: "#DDD6FE",
																		},
																		children: "KOTACOM PRESS",
																	},
																},
																{
																	type: "span",
																	props: {
																		style: {
																			fontSize: "11px",
																			color: "#A78BFA",
																			fontFamily: "JetBrains Mono",
																		},
																		children: "A5 / B5",
																	},
																},
															],
														},
													},
												],
											},
										},
										// Book Edge Pages (Cream Bookpaper)
										{
											type: "div",
											props: {
												style: {
													width: "28px",
													height: "308px",
													backgroundColor: "#FEF3C7",
													borderTopRightRadius: "4px",
													borderBottomRightRadius: "4px",
													border: "1px solid #FDE68A",
													marginLeft: "-2px",
												},
											},
										},
									],
								},
							},

							// Floating Badges on the right
							{
								type: "div",
								props: {
									style: {
										display: "flex",
										flexDirection: "column",
										gap: "16px",
										marginLeft: "48px",
									},
									children: [
										// Price Badge
										{
											type: "div",
											props: {
												style: {
													backgroundColor: "#FBBF24",
													color: "#000000",
													borderRadius: "14px",
													padding: "16px 24px",
													display: "flex",
													flexDirection: "column",
													gap: "4px",
													boxShadow: "0 10px 25px -5px rgba(251, 191, 36, 0.4)",
												},
												children: [
													{
														type: "span",
														props: {
															style: {
																fontSize: "13px",
																fontFamily: "JetBrains Mono",
																fontWeight: 700,
																letterSpacing: "0.05em",
															},
															children: "BIAYA CETAK",
														},
													},
													{
														type: "span",
														props: {
															style: {
																fontSize: "24px",
																fontWeight: 700,
															},
															children: price,
														},
													},
												],
											},
										},
										// Feature Badge 1
										{
											type: "div",
											props: {
												style: {
													backgroundColor: "rgba(16, 185, 129, 0.2)",
													border: "1px solid #10B981",
													borderRadius: "12px",
													padding: "12px 18px",
													display: "flex",
													alignItems: "center",
													gap: "10px",
												},
												children: [
													{
														type: "span",
														props: {
															style: {
																fontSize: "17px",
																fontWeight: 600,
																color: "#34D399",
															},
															children: "✓ Mesin Digital 1200 DPI",
														},
													},
												],
											},
										},
										// Feature Badge 2
										{
											type: "div",
											props: {
												style: {
													backgroundColor: "rgba(56, 189, 248, 0.2)",
													border: "1px solid #38BDF8",
													borderRadius: "12px",
													padding: "12px 18px",
													display: "flex",
													alignItems: "center",
													gap: "10px",
												},
												children: [
													{
														type: "span",
														props: {
															style: {
																fontSize: "17px",
																fontWeight: 600,
																color: "#7DD3FC",
															},
															children: "✓ Jilid Lem Panas Kuat",
														},
													},
												],
											},
										},
									],
								},
							},
						],
					},
				},

				// 4. BOTTOM 3 SELLING PILLS
				{
					type: "div",
					props: {
						style: {
							display: "flex",
							justifyContent: "space-between",
							gap: "16px",
							width: "100%",
							marginTop: "16px",
						},
						children: [
							{
								type: "div",
								props: {
									style: {
										flex: 1,
										backgroundColor: "#1E293B",
										borderRadius: "14px",
										padding: "16px 18px",
										display: "flex",
										flexDirection: "column",
										gap: "4px",
										border: "1px solid #334155",
									},
									children: [
										{
											type: "span",
											props: {
												style: {
													fontSize: "14px",
													fontWeight: 700,
													color: "#10B981",
												},
												children: "⚡ CETAK SATUAN",
											},
										},
										{
											type: "span",
											props: {
												style: {
													fontSize: "15px",
													color: "#CBD5E1",
												},
												children: "Mulai 1 eksemplar bebas",
											},
										},
									],
								},
							},
							{
								type: "div",
								props: {
									style: {
										flex: 1,
										backgroundColor: "#1E293B",
										borderRadius: "14px",
										padding: "16px 18px",
										display: "flex",
										flexDirection: "column",
										gap: "4px",
										border: "1px solid #334155",
									},
									children: [
										{
											type: "span",
											props: {
												style: {
													fontSize: "14px",
													fontWeight: 700,
													color: "#FBBF24",
												},
												children: "📖 KERTAS BOOKPAPER",
											},
										},
										{
											type: "span",
											props: {
												style: {
													fontSize: "15px",
													color: "#CBD5E1",
												},
												children: "Krem impor tidak tembus",
											},
										},
									],
								},
							},
							{
								type: "div",
								props: {
									style: {
										flex: 1,
										backgroundColor: "#1E293B",
										borderRadius: "14px",
										padding: "16px 18px",
										display: "flex",
										flexDirection: "column",
										gap: "4px",
										border: "1px solid #334155",
									},
									children: [
										{
											type: "span",
											props: {
												style: {
													fontSize: "14px",
													fontWeight: 700,
													color: "#38BDF8",
												},
												children: "🛡️ 100% GARANSI",
											},
										},
										{
											type: "span",
											props: {
												style: {
													fontSize: "15px",
													color: "#CBD5E1",
												},
												children: "Ganti baru jika cacat",
											},
										},
									],
								},
							},
						],
					},
				},

				// 5. FOOTER CALL-TO-ACTION BAR
				{
					type: "div",
					props: {
						style: {
							display: "flex",
							justifyContent: "space-between",
							alignItems: "center",
							width: "100%",
							borderTop: "1px solid #1E293B",
							paddingTop: "20px",
						},
						children: [
							{
								type: "span",
								props: {
									style: {
										fontFamily: "JetBrains Mono",
										fontSize: "18px",
										fontWeight: 600,
										color: "#10B981",
									},
									children: "WhatsApp: +62 857-9952-0350",
								},
							},
							{
								type: "span",
								props: {
									style: {
										fontFamily: "JetBrains Mono",
										fontSize: "16px",
										color: "#64748B",
									},
									children: "Workshop Kotacom Network • Kirim Se-Indonesia",
								},
							},
						],
					},
				},
			],
		},
	};
}

export async function renderSquareOgPng(node: Node): Promise<Buffer> {
	const svg = await satori(node as never, {
		width: SQUARE_SIZE,
		height: SQUARE_SIZE,
		fonts: loadFonts() as never,
	});
	return sharp(Buffer.from(svg)).png({ compressionLevel: 9 }).toBuffer();
}
